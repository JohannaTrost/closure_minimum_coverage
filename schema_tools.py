import copy

def get_non_maximal_schemas(schemas):
    '''
    Trouver dans un ensemble de schémas lesquels qui sont non-maximals.
    e.g. si il y'a R1(ABC) et R2(BC) R2 est redondant

    :param schemas: liste avec des schémas relationnels en dictionnaire
    :return: liste avec des schémas non-maximals
    '''

    redundant_schemas = []
    for i, schema in enumerate(schemas):
        for j, other_schema in enumerate(schemas):
            if i != j:
                if schema['attributes'] in other_schema['attributes']:
                    redundant_schemas.append(schema)
    return redundant_schemas


def join_all_schemas(schemas):
    schemas_joined = copy.deepcopy(schemas)
    join_possible = True
    while join_possible:
        joined_schema = {}
        for i, schema in enumerate(schemas_joined):
            for j, other_schema in enumerate(schemas_joined):
                if i != j:
                    if 0 < len(set(schema['attributes']).intersection(
                            other_schema['attributes'])):
                        joined_schema = natural_join(schema, other_schema)
                        break
            if len(joined_schema) > 0:
                break
        if len(joined_schema) == 0:
            join_possible = False
        else:
            schemas_joined.remove(schema)
            schemas_joined.remove(other_schema)
            schemas_joined.append(joined_schema)

    return schemas_joined


def natural_join(schema_r1, schema_r2):
    joined_schema = {
        'keys': sorted(''.join(set(schema_r1['keys']).union(schema_r2['keys']))),
        'attributes': sorted(''.join(set(schema_r1['attributes']).union(
                                         schema_r2['attributes'])))}
    return joined_schema
