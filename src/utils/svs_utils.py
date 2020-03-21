import enums


def get_SVS_level_ratio(resolution_level):
    if resolution_level == enums.ResolutionLevel.LEVEL_0_BASE:
        return enums.SVSLevelRatio.LEVEL_0_BASE
    elif resolution_level == enums.ResolutionLevel.LEVEL_1:
        return enums.SVSLevelRatio.LEVEL_1
    elif resolution_level == enums.ResolutionLevel.LEVEL_2:
        return enums.SVSLevelRatio.LEVEL_2
    elif resolution_level == enums.ResolutionLevel.LEVEL_3:
        return enums.SVSLevelRatio.LEVEL_3
