# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains round behaviours of TransactionPreparationAbciApp."""

from packages.valory.contracts.gnosis_safe.contract import GnosisSafeContract
from abc import ABC
from typing import Generator, Set, Type, cast, Optional
from packages.valory.protocols.contract_api import ContractApiMessage
from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
import json
from packages.valory.skills.transaction_preparation_abci.models import Params
from packages.valory.skills.transaction_preparation_abci.rounds import (
    SynchronizedData,
    TransactionPreparationAbciApp,
    TransactionPreparationAbciRound,
)
from packages.valory.skills.transaction_preparation_abci.rounds import (
    TransactionPreparationAbciPayload,
)
from packages.valory.skills.transaction_settlement_abci.payload_tools import (
    hash_payload_to_hex,
)

SAFE_TX_GAS = 0
ETHER_VALUE = 0


class TransactionPreparationBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the transaction_preparation_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class TransactionPreparationAbciBehaviour(TransactionPreparationBaseBehaviour):
    """TransactionPreparationAbciBehaviour"""

    matching_round: Type[AbstractRound] = TransactionPreparationAbciRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            votable_proposal_ids, proposals = self._get_proposal_info()

            finished_task_data = self.synchronized_data.finished_task_data

            # TODO: pass data to _get_safe_tx_hash
            tx_hash = yield from self._get_safe_tx_hash()

            if not tx_hash:
                tx_hash = TransactionPreparationAbciRound.ERROR_PAYLOAD

            payload_content = {
                "tx_hash": tx_hash,
                "proposals": proposals,
                "votable_proposal_ids": votable_proposal_ids,
            }

            payload = TransactionPreparationAbciPayload(
                sender=self.context.agent_address,
                content=json.dumps(payload_content, sort_keys=True),
            )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _get_safe_tx_hash(
        self,
    ) -> Generator[None, None, Optional[str]]:
        """Get the transaction hash of the Safe tx."""
        # Get the raw transaction from the Bravo Delegate contract
        contract_api_msg = yield from self.get_contract_api_response(
            performative=ContractApiMessage.Performative.GET_STATE,  # type: ignore
            contract_address=, # TODO
            contract_id=str(.contract_id), # TODO
            contract_callable="", # TODO
        )
        if (
            contract_api_msg.performative != ContractApiMessage.Performative.STATE
        ):  # pragma: nocover
            self.context.logger.warning(
                f"get_cast_vote_data unsuccessful!: {contract_api_msg}"
            )
            return None
        data = cast(bytes, contract_api_msg.state.body["data"])

        # Get the safe transaction hash
        ether_value = ETHER_VALUE
        safe_tx_gas = SAFE_TX_GAS

        contract_api_msg = yield from self.get_contract_api_response(
            performative=ContractApiMessage.Performative.GET_STATE,  # type: ignore
            contract_address=self.synchronized_data.safe_contract_address,
            contract_id=str(GnosisSafeContract.contract_id),
            contract_callable="get_raw_safe_transaction_hash",
            to_address=, # TODO
            value=ether_value,
            data=data,
            safe_tx_gas=safe_tx_gas,
        )
        if (
            contract_api_msg.performative != ContractApiMessage.Performative.STATE
        ):  # pragma: nocover
            self.context.logger.warning(
                f"get_raw_safe_transaction_hash unsuccessful!: {contract_api_msg}"
            )
            return None

        safe_tx_hash = cast(str, contract_api_msg.state.body["tx_hash"])
        safe_tx_hash = safe_tx_hash[2:]
        self.context.logger.info(f"Hash of the Safe transaction: {safe_tx_hash}")

        # temp hack:
        payload_string = hash_payload_to_hex(
            safe_tx_hash, ether_value, safe_tx_gas, governor_address, data  # TODO
        )

        return payload_string


class TransactionPreparationRoundBehaviour(AbstractRoundBehaviour):
    """TransactionPreparationRoundBehaviour"""

    initial_behaviour_cls = TransactionPreparationAbciBehaviour
    abci_app_cls = TransactionPreparationAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        TransactionPreparationAbciBehaviour
    ]
