# -*- coding: utf-8 -*-
from analysis.pipeline.analysis_pipeline import AnalysisPipeline
from analysis.permutation_analyzer import PermutationAnalyzer


def build_default_pipeline() -> AnalysisPipeline:

    """
    Builds the default research analysis pipeline.

    :return: The configured analysis pipeline.
    """

    pipeline = AnalysisPipeline()
    pipeline.register(PermutationAnalyzer())

    return pipeline
