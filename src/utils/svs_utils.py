from .enums import ResolutionLevel, SVSLevelRatio

def get_SVS_level_ratio(resolution_level):
    if resolution_level == ResolutionLevel.LEVEL_0_BASE:
        return SVSLevelRatio.LEVEL_0_BASE
    elif resolution_level == ResolutionLevel.LEVEL_1:
        return SVSLevelRatio.LEVEL_1
    elif resolution_level == ResolutionLevel.LEVEL_2:
        return SVSLevelRatio.LEVEL_2
    elif resolution_level == ResolutionLevel.LEVEL_3:
        return SVSLevelRatio.LEVEL_3
