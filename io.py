import calculs as c
import dependency_tools as dt
import argparse


def show_results(list_of_dfs, closures, closures_linear, min_coverages,
                 min_reduced_coverages, normalised_schema, dmvs):
    for i, dfs in enumerate(list_of_dfs):
        # affichage de l'ensemble
        print('______________________________________')
        print('{}. ENSEMBLE DE DFs DONNEES EN ENTREE'.format(i + 1))
        dt.show(dfs)

        # affichage de fermeture(s)
        if len(closures) > 0:
            print('______________________________________')
            print('FERMETURE(S)')
            for key, value in closures[i].items():
                print(key + u'\u207A' + ' = ' + value)

        # affichage de fermeture(s) calculées en utilisant l'algorithme lineaire
        if len(closures_linear) > 0:
            print('______________________________________')
            print('FERMETURE(S) ALGORITHME LINEAIRE')
            for key, value in closures_linear[i].items():
                print(key + u'\u207A' + ' = ' + value)

        # affichage du couverture minimal
        if len(min_coverages) > 0:
            print('______________________________________')
            print('COUVERTURE MINIMAL')
            dt.show(min_coverages[i])

        # affichage du couverture minimal reduite
        if len(min_reduced_coverages) > 0:
            print('______________________________________')
            print('COUVERTURE MINIMAL REDUITE')
            dt.show(min_reduced_coverages[i])
        print('\n______________________________________')

        # affichage du schéma normalisé
        if len(normalised_schema) > 0:
            print('NORMALISATION')
            print('\nEnsemble de DMVs:')
            dt.show_dmvs(dmvs)
            print('\nSchéma normalisé:')
            for i, r in enumerate(normalised_schema):
                keys = "\u0332".join("{} ".format(r['keys']))
                attributes = ''.join(set(r['attributes']).difference(r['keys']))
                print('R{}({}{})'.format((i+1), keys, attributes))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('DFs', type=str, default=['df_ex_0.txt'], nargs='*',
                        help="Le chemin d'accès au fichier .txt qui contient "
                             "un ensemble de DFs. Il y a un ensemble de DFs "
                             "par defaut. Vous pouvez donner plusieurs "
                             "fichiers.")
    parser.add_argument('-f', '--fermeture', type=str, nargs='*',
                        help="la fermeture des attributs données de "
                             "l'ensemble de DFs donné est calculée et "
                             "affichée")
    parser.add_argument('-fl', '--fermeture_lineaire', type=str, nargs='*',
                        help="la fermeture des attributs données de "
                             "l'ensemble de DFs donné est calculée et "
                             "affichée en utilisant l'algorithme linéaire")
    parser.add_argument('-m', '--couverture_minimal', action='store_true',
                        help="la couverture minimal de l'ensemble de DFs "
                             "donné est calculée et affichée")
    parser.add_argument('-r', '--couverture_minimal_reduite',
                        action='store_true',
                        help="la couverture minimal et réduite de l'ensemble "
                             "de DFs donné est calculée et affichée")
    parser.add_argument('-n', '--normalisation', type=str,
                        default='',
                        help="Le chemin d'accès au fichier .txt qui contient "
                             "un ensemble de DMVs. Seulement s'il n'y a qu'un "
                             "seul ensemble de DFs donné")

    args = parser.parse_args()

    list_of_dfs = []
    closures = []
    closures_linear = []
    min_coverages = []
    min_reduced_coverages = []
    normalised_schema = []
    dmvs = []

    for i, dfs_file in enumerate(args.DFs):
        list_of_dfs.append(dt.txt_to_dependency(dfs_file))
        if args.fermeture:
            closures_per_dfs = {}
            for attr in args.fermeture:
                closures_per_dfs[attr] = c.closure_attributes(list_of_dfs[i],
                                                               attr)
            closures.append(closures_per_dfs)
        if args.fermeture_lineaire:
            closures_per_dfs_lin = {}
            for attr in args.fermeture_lineaire:
                closures_per_dfs_lin[attr] = c.linear_closure_attributes(
                    list_of_dfs[i], attr)
            closures_linear.append(closures_per_dfs_lin)
        if args.couverture_minimal:
            min_coverages.append(c.minimal_coverage(list_of_dfs[i]))
        if args.couverture_minimal_reduite:
            min_reduced_coverages.append(c.df_reduction(list_of_dfs[i]))
        if args.normalisation:
            if len(list_of_dfs) > 1:
                raise IOError(
                    "Veuillez ne spécifier qu'un seul fichier avec les DF si " +
                    "vous voulez procéder à la normalisation. Sinon, il " +
                    "n'est pas clair à quel ensemble de DF appartient " +
                    "l'ensemble des DMV.")
            else:
                dmvs = dt.txt_to_dependency(args.normalisation)
                normalised_schema = c.synthesis(list_of_dfs[0], dmvs)

    show_results(list_of_dfs,
                 closures,
                 closures_linear,
                 min_coverages,
                 min_reduced_coverages,
                 normalised_schema,
                 dmvs)


if __name__ == "__main__":
    main()
