import json
import logging
import collections
from jsonpath_ng import jsonpath, parse

logger = logging.getLogger(__name__)


def jsonpath(path, obj, allow_none=False):
    r = [m.value for m in parse(path).find(obj)]
    return r[0] if not allow_none else (r[0] if r else None)


def listize(obj):
    return obj if (obj is None or isinstance(obj, list)) else [obj]


def get_booltest_info(results, cursor, variant_id):
    if not results:
        return None
    try:
        js = json.loads(results[0].message, object_pairs_hook=collections.OrderedDict)
        res = js["inputs"][0]["res"]
        js["halving"] = jsonpath('$.halving', js, True) or False
        js["time_elapsed"] = jsonpath('$.time_elapsed', js, True)
        js["best_dist"] = jsonpath('$[0].dists[0]', res, True)
        js["best_dist_poly"] = jsonpath('$[0].dists[0].poly', res, True)
        js["best_dist_zscore"] = jsonpath('$[0].dists[0].zscore', res, True)
        js["best_dist_halving"] = jsonpath('$[1].halvings[0]', res, True) if js["halving"] else None
        js["ref_samples"] = jsonpath('$[0].ref_samples', res, True)
        js["ref_alpha"] = jsonpath('$[0].ref_alpha', res, True)
        js["ref_zscore_min"] = jsonpath('$[0].ref_minmax[0]', res, True)
        js["ref_zscore_max"] = jsonpath('$[0].ref_minmax[1]', res, True)
        js["rejects"] = jsonpath('$[0].rejects', res, True)
        if js["halving"]:
            js["best_dist_zscore_halving"] = jsonpath('$[1].dists[0].zscore', res, True)
            js["pval"] = jsonpath('$.pval', js["best_dist_halving"], True)
        return js

    except Exception as e:
        logger.info("Exception parsing BoolTest results: %s" % (e,), exc_info=e)
