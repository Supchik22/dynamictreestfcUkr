from mcresources import ResourceManager, utils


def generate(rm: ResourceManager):

    dt_worldgen_definition(rm)

    for name in ALL_SPECIES:
        species(rm, name)
        family(rm, name)
        leaves_properties(rm, name)
        basic_tree_assets(rm, name)

    for soil in DIRT_TYPES:
        soil_properties(rm, soil, 'mud')
        soil_properties(rm, soil, 'dirt')
        soil_properties(rm, soil, 'farmland', ident('%s_dirt' % soil))
        soil_properties(rm, soil, 'rooted_dirt', ident('%s_dirt' % soil))
        soil_properties(rm, soil, 'grass', ident('%s_dirt' % soil))


def basic_tree_assets(rm: ResourceManager, name: str):
    branch = rm.blockstate('%s_branch' % name).with_lang(lang('%s branch', name))
    strip = rm.blockstate('stripped_%s_branch' % name).with_lang(lang('stripped %s branch', name))
    leaf = rm.blockstate('%s_leaves' % name, model='tfc:block/wood/leaves/%s' % name).with_lang(lang('%s leaves', name))
    sap = rm.blockstate('%s_sapling' % name).with_lang(lang('%s sapling', name))

    sap.with_block_model(parent='dynamictrees:block/smartmodel/sapling', textures={
        'particle': 'tfc:block/wood/leaves/%s' % name,
        'log': 'tfc:block/wood/log/%s' % name,
        'leaves': 'tfc:block/wood/leaves/%s' % name
    })
    rm.custom_block_model('%s_branch' % name, 'dynamictrees:branch', {'textures': {
        'bark': 'tfc:block/wood/log/%s' % name,
        'rings': 'tfc:block/wood/log_top/%s' % name,
    }})
    rm.custom_block_model('stripped_%s_branch' % name, 'dynamictrees:branch', {'textures': {
        'bark': 'tfc:block/wood/stripped_log/%s' % name,
        'rings': 'tfc:block/wood/stripped_log_top/%s' % name,
    }})
    rm.item_model('%s_branch' % name, {
        'bark': 'tfc:block/wood/log/%s' % name,
        'rings': 'tfc:block/wood/log_top/%s' % name,
    }, parent='dynamictrees:item/branch')
    rm.item_model('%s_seed' % name, {'layer0': 'dttfc:item/seed/%s' % name}, parent='dynamictrees:item/standard_seed').with_lang(lang('%s seed', name))

    branch.with_tag('dynamictrees:branches_that_burn')
    strip.with_tag('dynamictrees:branches_that_burn')
    branch.with_tag('dynamictrees:branches')
    strip.with_tag('dynamictrees:branches')
    leaf.with_tag('dynamictrees:leaves')
    sap.with_tag('dynamictrees:saplings')

    branch.with_block_loot()
    sap.with_block_loot()
    leaf.with_block_loot()

    rm.block_tag('dynamictrees:foliage', '#tfc:plants')


def soil_properties(rm: ResourceManager, name: str, tfc_soil: str, sub: str = None):
    if sub is None:
        block = rm.blockstate('rooty_%s_%s' % (name, tfc_soil)).with_lang(lang('rooty %s %s', name, tfc_soil)).with_block_model().with_block_loot('tfc:%s/%s' % (tfc_soil, name)).with_item_model()
    write(rm, 'soil_properties', name + '_' + tfc_soil, {
        'primitive_soil': 'tfc:%s/%s' % (tfc_soil, name),
        'acceptable_soils': ['dirt_like'],
        'substitute_soil': sub
    })


def species(rm: ResourceManager, name: str):
    res = ident(name)
    write(rm, 'species', name, {
        'family': res,
        #'can_bone_meal_tree': False (for testing)
    })


def family(rm: ResourceManager, name: str):
    res = ident(name)
    write(rm, 'families', name, {
        'common_species': res,
        'common_leaves': res,
        'primitive_log': 'tfc:wood/log/%s' % name,
        'primitive_stripped_log': 'tfc:wood/stripped_log/%s' % name,
    })


def leaves_properties(rm: ResourceManager, name: str):
    write(rm, 'leaves_properties', name, {
        'primitive_leaves': 'tfc:wood/leaves/%s' % name
    })


def dt_worldgen_definition(rm: ResourceManager):
    species_list = {}
    for s in ALL_SPECIES:
        species_list[s.replace('\'', '"')] = 1  # mcresources bug lol
    utils.write((*rm.resource_dir, 'trees', rm.domain, 'world_gen', 'default'), [
        {
            'select': {
                'names_or': ['tfc:.*']  # regex
            },
            'cancellers': {
                'type': ident('forest'),
            }
        },
        {
            'select': {
                'names_or': ['tfc:%s' % b for b in LAND_BIOMES],
                'apply': {
                    'species': {
                        'method': 'replace',
                        'random': species_list
                    }
                }
            }
        }
    ], on_error=on_error)


def write(rm: ResourceManager, folder: str, path: str, data):
    rm.write((*rm.resource_dir, 'trees', rm.domain, folder, path), data)


def ident(path: str) -> str:
    return utils.resource_location('dttfc', path).join()


def on_error(error: str, e: Exception):
    print(error)
    raise e


def lang(key: str, *args) -> str:
    return ((key % args) if len(args) > 0 else key).replace('_', ' ').replace('/', ' ').title()


ALL_SPECIES = ['pine', 'oak', 'blackwood']
LAND_BIOMES = ['plains', 'hills', 'lowlands', 'low_canyons', 'rolling_hills', 'badlands', 'inverted_badlands', 'plateau', 'canyons', 'mountains', 'old_mountains', 'oceanic_mountains', 'volcanic_mountains', 'volcanic_oceanic_mountains']
DIRT_TYPES = ['sandy_loam', 'loam', 'silty_loam', 'silt']