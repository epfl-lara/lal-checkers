"""
Output the JSON-formatted results of the "collecting semantics" analysis.
"""

from checkers.check_variants import check_variants
import collecting_semantics_helpers
import test_helper

import json
import os


def format_analysis_results(results):
    return json.dumps({
        pred_name: [
            {
                'trace': sorted([n.name for n in trace]),
                'precise': precise
            }
            for trace, _, precise in analysis.infeasibles
        ]
        for pred_name, analysis in results.iteritems()
    }, sort_keys=True, indent=2)


@test_helper.run
def run(args):
    results = collecting_semantics_helpers.do_analysis(
        check_variants,
        collecting_semantics_helpers.default_merge_predicates
    )

    if args.output_dir is not None:
        test_helper.ensure_dir(args.output_dir)

    for pred_name, analysis in results.iteritems():
        if args.output_dir is not None:
            analysis.sem_analysis.save_cfg_to_file(os.path.join(
                args.output_dir,
                'cfg.dot'
            ))
            analysis.sem_analysis.save_results_to_file(os.path.join(
                args.output_dir,
                'sem_{}.dot'.format(pred_name)
            ))
            analysis.save_results_to_file(os.path.join(
                args.output_dir,
                'field_exists_{}.dot'.format(pred_name)
            ))

    print(str(format_analysis_results(results)))
