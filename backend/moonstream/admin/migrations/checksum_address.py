"""
Convert all addresses in user subscriptions 
and ethereum_labels column to checksum address.
"""
import logging

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException
from moonstreamdb.models import EthereumLabel
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from web3 import Web3

from ...settings import BUGOUT_REQUEST_TIMEOUT_SECONDS, MOONSTREAM_ADMIN_ACCESS_TOKEN
from ...settings import bugout_client as bc

logger = logging.getLogger(__name__)


def checksum_all_subscription_addresses(web3: Web3) -> None:
    """
    Parse all existing subscriptions at Brood resource
    and replace address with checksum.
    """
    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": "subscription"},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    for resource in resources.resources:
        resource_data = resource.resource_data
        try:
            address = resource_data["address"]
            resource_data["address"] = web3.toChecksumAddress(address)
            updated_resource = bc.update_resource(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                resource_id=resource.id,
                resource_data={"update": resource_data},
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
            logger.info(f"Resource id: {updated_resource.id} updated")
        except ValueError as e:
            logger.info(
                f"Not valid checksum address: {address}, probably "
                "txpool or whalewatch subscription"
            )
            continue
        except BugoutResponseException as e:
            logger.info(f"Bugout error: {e.status_code} with details: {e.detail}")
        except Exception as e:
            logger.info(f"Unexpected error: {repr(e)}")
            continue


def checksum_all_labels_addresses(db_session: Session, web3: Web3) -> None:
    """
    Convert all address to checksum in ethereum_labels column at database.

    Docs for SQLAlchemy mapping:
    https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings
    """
    query_limit = 500

    while True:
        query = (
            db_session.query(EthereumLabel.id, EthereumLabel.address)
            .filter(EthereumLabel.address == func.lower(EthereumLabel.address))
            .limit(query_limit)
        )
        address_list = query.all()
        address_list_len = len(address_list)
        if address_list_len == 0:
            break

        logger.info(f"Updating next {address_list_len} rows")

        # Build map of id and updated address checksum
        mappings = []
        for address in address_list:
            mappings.append(
                {"id": address[0], "address": web3.toChecksumAddress(address[1])}
            )
        db_session.bulk_update_mappings(EthereumLabel, mappings)
        db_session.commit()
        mappings[:] = []

