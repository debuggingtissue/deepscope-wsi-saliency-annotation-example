from .enums import ResolutionLevel


def get_SVS_level_ratio(svs_image, from_resolution_level, to_resolution_level):
    if from_resolution_level == ResolutionLevel.THUMBNAIL:
        from_resolution_level_width = svs_image.associated_images["thumbnail"].size[0]
    else:
        from_resolution_level_width = svs_image.level_dimensions[from_resolution_level][0]

    if to_resolution_level == ResolutionLevel.THUMBNAIL:
        to_resolution_level_width = svs_image.associated_images["thumbnail"].size[0]
    else:
        to_resolution_level_width = svs_image.level_dimensions[to_resolution_level][0]

    if from_resolution_level >= to_resolution_level:
        ratio = (to_resolution_level_width / from_resolution_level_width)
    else:
        ratio = (from_resolution_level_width / to_resolution_level_width)

    return ratio
