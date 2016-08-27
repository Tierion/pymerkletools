import hashlib
from math import sqrt
from merkletools import MerkleTools


def test_add_leaf():
    mt = MerkleTools()
    mt.add_leaf("tierion", do_hash=True)
    mt.add_leaf(["bitcoin", "blockchain"], do_hash=True)
    assert mt.get_leaf_count() == 3
    assert mt.is_ready == False

def test_build_tree():
    mt = MerkleTools()
    mt.add_leaf("tierion", do_hash=True)
    mt.add_leaf(["bitcoin", "blockchain"], do_hash=True)
    mt.make_tree()
    assert mt.is_ready == True
    mt.get_merkle_root() == '765f15d171871b00034ee55e48ffdf76afbc44ed0bcff5c82f31351d333c2ed1'


def test_get_proof():
    mt = MerkleTools()
    mt.add_leaf("tierion", do_hash=True)
    mt.add_leaf(["bitcoin", "blockchain"], do_hash=True)
    mt.make_tree()
    proof_1 = mt.get_proof(1)
    for p in proof_1:
        try:
            assert p['left'] == '2da7240f6c88536be72abe9f04e454c6478ee29709fc3729ddfb942f804fbf08'
        except:
            assert p['right'] == 'ef7797e13d3a75526946a3bcf00daec9fc9c9c4d51ddc7cc5df888f74dd434d1'


# Standard tests
def test_basics():
    bLeft = 'a292780cc748697cb499fdcc8cb89d835609f11e502281dfe3f6690b1cc23dcb'
    bRight = 'cb4990b9a8936bbc137ddeb6dcab4620897b099a450ecdc5f3e86ef4b3a7135c'
    mRoot = hashlib.sha256(bLeft.decode('hex') + bRight.decode('hex')).hexdigest()

    # tree with no leaves
    mt = MerkleTools()
    mt.make_tree()
    assert mt.get_merkle_root() is None

    # tree with hex add_leaf
    mt.add_leaf([bLeft, bRight])
    mt.make_tree()
    assert mt.get_merkle_root() == mRoot


def test_bad_hex():
    # try to add bad hex
    mt = MerkleTools()
    try:
        mt.add_leaf('nothexandnothashed')
        assert False   # should not get here!
    except:
        pass


def test_one_leaf():
    # make tree with one leaf
    mt = MerkleTools()
    mt.add_leaf(['ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', ])
    mt.make_tree()
    assert mt.get_merkle_root() == 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb'


def test_5_leaves():
    mt = MerkleTools()
    mt.add_leaf([
        'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb',
        '3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d',
        '2e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6',
        '18ac3e7343f016890c510e93f935261169d9e3f565436429830faf0934f4f8e4',
        '3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea'
    ])
    mt.make_tree()
    assert mt.get_merkle_root() == 'd71f8983ad4ee170f8129f1ebcdd7440be7798d8e1c80420bf11f1eced610dba'


def test_unhashed_leaves():
    mt = MerkleTools()
    mt.add_leaf('a', True)
    mt.add_leaf('b', True)
    mt.add_leaf('c', True)
    mt.add_leaf('d', True)
    mt.add_leaf('e', True)
    mt.make_tree()
    assert mt.get_merkle_root() == 'd71f8983ad4ee170f8129f1ebcdd7440be7798d8e1c80420bf11f1eced610dba'

    mt.reset_tree()
    mt.add_leaf(['a', 'b', 'c', 'd', 'e'], True)
    mt.make_tree()
    assert mt.get_merkle_root() == 'd71f8983ad4ee170f8129f1ebcdd7440be7798d8e1c80420bf11f1eced610dba'


def test_md5_tree():
    bLeftmd5 = '0cc175b9c0f1b6a831c399e269772661'
    bRightmd5 = '92eb5ffee6ae2fec3ad71c777531578f'
    mRootmd5 = hashlib.md5(bLeftmd5.decode('hex')+bRightmd5.decode('hex')).hexdigest()

    mt = MerkleTools('md5')
    mt.add_leaf([bLeftmd5, bRightmd5])
    mt.make_tree()
    assert mt.get_merkle_root() == mRootmd5


def test_proof_nodes():
    bLeft = 'a292780cc748697cb499fdcc8cb89d835609f11e502281dfe3f6690b1cc23dcb'
    bRight = 'cb4990b9a8936bbc137ddeb6dcab4620897b099a450ecdc5f3e86ef4b3a7135c'
    mRoot = hashlib.sha256(bLeft.decode('hex') + bRight.decode('hex')).hexdigest()

    mt = MerkleTools()
    mt.add_leaf(bLeft)
    mt.add_leaf(bRight)
    mt.make_tree()
    proof = mt.get_proof(0)
    assert proof[0]['right'] == 'cb4990b9a8936bbc137ddeb6dcab4620897b099a450ecdc5f3e86ef4b3a7135c'
    proof = mt.get_proof(1)
    assert proof[0]['left'] == 'a292780cc748697cb499fdcc8cb89d835609f11e502281dfe3f6690b1cc23dcb'


def test_proof_no_leaves():
    mt = MerkleTools()
    mt.make_tree()
    proof = mt.get_proof(0)
    assert proof is None


def test_bad_proof():
    bLeft = 'a292780cc748697cb499fdcc8cb89d835609f11e502281dfe3f6690b1cc23dcb'
    bRight = 'cb4990b9a8936bbc137ddeb6dcab4620897b099a450ecdc5f3e86ef4b3a7135c'

    mt = MerkleTools()
    mt.add_leaf(bLeft)
    mt.add_leaf(bRight)
    mt.make_tree()
    proof = mt.get_proof(1)
    is_valid = mt.validate_proof(proof, bRight, bLeft)
    assert not is_valid


def test_validate_5_leaves():
    mt = MerkleTools()
    mt.add_leaf([
        'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb',
        '3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d',
        '2e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6',
        '18ac3e7343f016890c510e93f935261169d9e3f565436429830faf0934f4f8e4',
        '3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea'
    ])
    mt.make_tree()

    # bad proof
    proof = mt.get_proof(3)
    is_valid = mt.validate_proof(proof, 'badc3e7343f016890c510e93f935261169d9e3f565436429830faf0934f4f8e4', 'd71f8983ad4ee170f8129f1ebcdd7440be7798d8e1c80420bf11f1eced610dba')
    assert is_valid == False

    # good proof
    proof = mt.get_proof(4)
    print proof
    is_valid = mt.validate_proof(proof, '3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea', 'd71f8983ad4ee170f8129f1ebcdd7440be7798d8e1c80420bf11f1eced610dba')
    assert is_valid == True

    proof = mt.get_proof(1)
    is_valid = mt.validate_proof(proof, '3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d', 'd71f8983ad4ee170f8129f1ebcdd7440be7798d8e1c80420bf11f1eced610dba')
    assert is_valid == True


if __name__ == "__main__":
    test_validate_5_leaves()
