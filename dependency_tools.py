import numpy as np

def show(dfs):
    """
    Affichage des DFs [[X, Y], [W, Z]] ~> X -> Y
                                          W -> Z

    :param dfs: liste des listes de DFs
    """

    for df in dfs:
        print('{} -> {}'.format(df[0], df[1]))


def show_dmvs(dmvs):
    """
    Affichage des DMVs [[X, Y], [W, Z]] ~> X ->-> Y
                                          W ->-> Z

    :param dfs: liste des listes de DMVs
    """

    for df in dmvs:
        print('{} ->-> {}'.format(df[0], df[1]))


def txt_to_dependency(fname):
    """
    Un ensemble de DFs est mis en place à partir d'un fichier txt

    :param fname: un string contenant le chemin vers le fichier txt
    (/mon/chemin/fichier.txt)
    :return: une liste de listes contenant les DFs

    """

    if fname[-3:] == 'txt':
        dependencies = np.loadtxt(fname, dtype=str)
        if len(np.shape(dependencies)) == 1:
            return [dependencies.tolist()]
        else:
            return dependencies.tolist()
    else:
        raise IOError("{} n'est pas un fichier txt!".format(fname))

