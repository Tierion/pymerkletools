import hashlib
from math import sqrt
from merkletools import MerkleTools


def test_add_left():
    mt = MerkleTools()
    mt.add_leaf("tierion")
    mt.add_leaf(["bitcoin", "blockchain"])
    assert mt.get_leaf_count() == 3
    assert mt.is_ready == False
    mt.make_tree()
    assert mt.is_ready == True
    print "root:", mt.get_merkle_root().encode('hex')
    print mt.get_proof(1)
    print mt.validate_proof(mt.get_proof(1), mt.get_leaf(1), mt.get_merkle_root())


def test_build_tree():
    mt = MerkleTools()
    mt.add_leaf("tierion")
    mt.add_leaf(["bitcoin", "blockchain"])
    mt.make_tree()
    assert mt.is_ready == True
    mt.get_merkle_root() == '765f15d171871b00034ee55e48ffdf76afbc44ed0bcff5c82f31351d333c2ed1'


def test_get_proof():
    mt = MerkleTools()
    mt.add_leaf("tierion")
    mt.add_leaf(["bitcoin", "blockchain"])
    mt.make_tree()
    proof_1 = mt.get_proof(1)
    assert proof_1['left'] == '2da7240f6c88536be72abe9f04e454c6478ee29709fc3729ddfb942f804fbf08'
    assert proof_1['right'] == 'ef7797e13d3a75526946a3bcf00daec9fc9c9c4d51ddc7cc5df888f74dd434d1'
