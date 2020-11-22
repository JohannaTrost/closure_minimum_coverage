import random
from itertools import combinations
import copy
import schema_tools as st

def closure_attributes(dfs, attributes):
    """
    La fermeture d'un ensemble d'attributs décide de l’implication logique
    des DFs selon Algorithme 1 de TP_Prog

    :param dfs: une liste des listes contenant les DFs
    :param attributes: l'ensemble d'attributs en string
    :return: un string avec la fermeture
    """

    closure = str(attributes)
    unused = copy.deepcopy(dfs)  # les dfs pas encore traitées
    some_left_to_check = True
    while some_left_to_check:  # la boucle est terminée s'il n'y avait pas un
        # ajout à la fermeture pendant l'itération précédent
        some_left_to_check = False
        for df in unused:
            if all(attr in closure for attr in df[0]):
                change = ''.join(
                    [attr for attr in df[1] if attr not in closure])
                if len(change) > 0:
                    closure += change
                some_left_to_check = True
                unused.remove(df)
                break
    return ''.join(sorted(closure, key=str.upper))


def linear_closure_attributes(dfs, attributes):
    """
    Version linéaire de l'algorithme de fermeture selon l'algorithme donné en
    cours

    :param dfs: une liste des listes contenant les DFs
    :param attributes: l'ensemble d'attributs en string
    :return: un string avec la fermeture
    """

    count = {}  # stocke le nombre d’attributs de X non encore dans closure
    # pour chaque X -> Y
    dict_all_attributes = {}  # dict pour chaque attribut A des DFs pour les
    # quelles A apparaît en partie gauche
    for df in dfs:
        count[str(df)] = len(df[0])
        for attribute in df[0]:
            if attribute in dict_all_attributes.keys():
                dict_all_attributes[attribute].append(df)
            else:
                dict_all_attributes[attribute] = [df]
    closure = str(attributes)
    update = str(attributes)
    while len(update) != 0:
        remove = random.randint(0, len(update) - 1)
        curr_attr = update[remove]
        update = update.replace(curr_attr, '')
        for df in dict_all_attributes[curr_attr]:
            count[str(df)] -= 1
            if count[str(df)] == 0:
                update += ''.join(
                    [attr for attr in df[1] if attr not in closure])
                closure += ''.join(
                    [attr for attr in df[1] if attr not in closure])
    return closure


def minimal_coverage(dfs):
    """
    Calcul d'une couverture minimum donc non redondante pour l'ensemble de DFs
    Algorithme 2 de TP_Prog

    :param dfs: liste des listes de DFs
    :return: liste des listes de DFs de la couverture minimum
    """

    min_coverage = []
    for df in dfs:
        new_df = [df[0],
                  closure_attributes(dfs + [], df[0])]  # X -> X+ pour X -> Y
        if new_df not in min_coverage:
            min_coverage.append(new_df)

    dfs_to_remove = []
    for df in min_coverage:
        min_coverage_without_df = [df_tmp for df_tmp in min_coverage if
                                   df_tmp != df]
        if is_satisfied(min_coverage_without_df, df):
            dfs_to_remove.append(df)
    # min_coverage − dfs_to_remove
    return [df for df in min_coverage if df not in dfs_to_remove]


def df_reduction(dfs):
    """
    Calcul d’une couverture "canonique" (minimum +réduction parties gauches
    et droites) Algorithme 3 de TP_Prog

    :param min_coverage: liste des listes de DFs
    :return: liste des listes de DFs de la couverture minimum réduite
    """

    reduced_coverage = minimal_coverage(
        dfs)  # au cas où les DFs en entrée ne sont pas une couverture minimale

    # df_reduction des parties gauches
    for df in reduced_coverage:
        left = str(df[0])
        right = df_reduce_right_side(df, reduced_coverage)
        if left != df[0]:
            reduced_coverage = [[left, right] if item == df else item for
                                item in reduced_coverage]

    # df_reduction des parties droites
    for df in reduced_coverage:
        left = str(df[0])
        right = df_reduce_right_side(df, reduced_coverage)
        if right != df[1]:
            reduced_coverage = [[left, right] if item == df else item for
                                item in reduced_coverage]

    return reduced_coverage


def df_reduce_left_side(df, dfs):
    """
    Réduction de la partie gauche d'une DF

    :param df: une liste contenant la DF
    :param dfs: liste des listes de DFs
    :return: la partie gauche de la DF comme string réduite si possible
    """

    left = str(df[0])
    sub_sets_left = [left[x:y] for x, y in combinations(
        range(len(left) + 1), r=2)]  # tous sous-ensembles de partie gauche
    random.shuffle(sub_sets_left)
    reduced_by = ''
    for sub_set in sub_sets_left:
        if len(left) == 1:
            # arrêt car la partie droite ne peut plus être réduite
            break
        if any([c for c in reduced_by if c in sub_set]):
            # ne plus tester les sous-strings avec un attribut déjà supprimé
            continue

        reduced_sub_string = left.replace(sub_set,
                                          '')  # reduire partie gauche (W - A)
        if is_satisfied(dfs, [reduced_sub_string, left]):  # Min |= (W − A) → X
            left = reduced_sub_string
            reduced_by += sub_set
    return left


def df_reduce_right_side(df, dfs):
    """
    Réduction de la partie droite d'une DF

    :param df: une liste contenant la DF
    :param dfs: liste des listes de DFs
    :return: la partie droite de la DF comme string réduite si possible
    """

    left = str(df[0])
    right = str(df[1])

    sub_sets_right = [right[x:y] for x, y in combinations(
                range(len(right) + 1), r=2)]
    random.shuffle(sub_sets_right)
    reduced_by = ''
    for sub_set in sub_sets_right:
        if len(right) == 1:
            # arrêt car la partie droite ne peut plus être réduite
            break
        if any([c for c in reduced_by if c in sub_set]):
            continue

        reduced_sub_string = right.replace(sub_set, '')
        tmp_dfs = [[left, reduced_sub_string] if item == df else item
                   for item in dfs]
        if is_satisfied(tmp_dfs, df):
            right = reduced_sub_string
            reduced_by += sub_set
    return right


def is_satisfied(epsilon, df):
    """
    Décide si un ensemble de DFs epsilon satisfait un DF X -> Y en calculant la
    fermeture de X.
    Si Y est inclu dans cette fermeture alors epsilon satisfait la DF

    :param epsilon: liste des listes de DFs
    :param df: liste répresentant la DF
    :return: true si epsilon satisfait df, false sinon
    """

    closure = closure_attributes(epsilon, df[0])
    if all(attribute in closure for attribute in df[1]):
        return True
    else:
        return False


def synthesis(dfs, dmvs):
    """
    L'algo donne un schéma en 3FN ou en FNBC quand c’est possible sans perte
    de dépendance

    :param dfs: liste des listes de DFs
    :param dmvs: liste des listes de DMVs
    :return: liste avec des schémas relationnels en dictionnaire
    """

    reduced_coverage = df_reduction(dfs)

    set_of_schemas = []
    # création de R(key(X)Y) pour chaque DF: X -> Y
    for df in reduced_coverage:
        relational_schema = {'keys': df[0], 'attributes': df[0] + df[1]}
        set_of_schemas.append(relational_schema)

    # création de R(lkey(X)Y') pour chaque X ->-> Y
    # alors que F satisfait Y' -> Y
    if len(dmvs) > 0:  # car ensemble de DMVs est optional
        schemas_from_dmvs = dmv_reduction(dmvs, dfs)
        set_of_schemas += schemas_from_dmvs

    # suppression des schémas non-maximal
    redondant_schemas = st.get_non_maximal_schemas(set_of_schemas)
    for schema in redondant_schemas:
        set_of_schemas.remove(schema)

    # vérifier s'il y a une perte de jointure
    schemas_joined = st.join_all_schemas(set_of_schemas)
    if len(schemas_joined) > 1:
        keys = ''.join([schema['keys'][0] for schema in schemas_joined])
        relational_schema = {'keys': keys, 'attributes': keys}
        set_of_schemas.append(relational_schema)

    return set_of_schemas


def dmv_reduction(dmvs, dfs):
    """
    Réduction de la partie droite des DMVs

    :param dfs: liste des listes de DFs
    :param dmvs: liste des listes de DMVs
    :return: schéma à partir des DMVs réduites
    """
    schemas = []
    for dmv in dmvs:
        right = dmv[1]
        # df_reduction de la partie droite de la DMV
        sub_sets = [right[x:y] for x, y in combinations(
            range(len(dmv[1]) + 1), r=2)]
        reduced_by = ''
        for sub_set in sub_sets:
            if len(right) == 1:
                break
            elif any([c for c in reduced_by if c in sub_set]):
                continue
            elif is_satisfied(dfs, [sub_set, right]):
                right = sub_set
                reduced_by += sub_set
        attributes_schema = ''.join(set(dmv[0]).union(right))
        schemas.append(
            {'keys': attributes_schema, 'attributes': attributes_schema})
    return schemas
