import hashlib
import json

import algosdk
from algosdk.v2client import algod
from beaker import sandbox
from algosdk.transaction import AssetCreateTxn, wait_for_confirmation, AssetOptInTxn, AssetTransferTxn


def mintNFT(algod_client, creator_address, creator_private_key, asset_name, asset_unit_name):
    # create asset
    sp = algod_client.suggested_params()
    txn = AssetCreateTxn(creator_address, sp, 1, 0, False, asset_name=asset_name, unit_name=asset_unit_name)
    signed_txn = txn.sign(creator_private_key)
    txid = algod_client.send_transaction(signed_txn)
    txn_result = wait_for_confirmation(algod_client, txid, 4)
    # return index of created asset
    return txn_result['asset-index']


def transferNFT(algod_client, creator_address, creator_private_key, receiver_address, receiver_private_key, asset_id):
    # opt-in receiver to asset
    sp = algod_client.suggested_params()
    txn0 = AssetOptInTxn(receiver_address, sp, asset_id)
    signed_txn0 = txn0.sign(receiver_private_key)
    txid0 = algod_client.send_transaction(signed_txn0)
    wait_for_confirmation(algod_client, txid0, 4)
    # transfer asset
    sp = algod_client.suggested_params()
    txn1 = AssetTransferTxn(creator_address, receiver_address, sp, asset_id, 1)
    signed_txn1 = txn1.sign(creator_private_key)
    txid1 = algod_client.send_transaction(signed_txn1)
    wait_for_confirmation(algod_client, txid1, 4)
