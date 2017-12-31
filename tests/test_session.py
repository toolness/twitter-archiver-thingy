from twitblog.session import StatusStats


def test_statusstats_as_params_works():
    assert StatusStats.empty().as_params(older=False) == {}
    assert StatusStats.empty().as_params(older=True) == {}
    assert StatusStats('1', '5').as_params(older=True) == {
        'max_id': '1'
    }
    assert StatusStats('1', '5').as_params(older=False) == {
        'since_id': '5'
    }


def test_statusstats_update_works():
    assert StatusStats.empty().update('5') == ('5', '5')
    assert StatusStats('1', '6').update('5') == ('1', '6')
    assert StatusStats('6', '7').update('5') == ('5', '7')
    assert StatusStats('1', '4').update('5') == ('1', '5')


def test_statusstats_from_cache_works():
    assert StatusStats.from_cache(None) == (None, None)
    assert StatusStats.from_cache(['1', '2']) == ('1', '2')
