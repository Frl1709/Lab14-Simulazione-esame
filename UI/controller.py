import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()
        nN, nE = self._model.getGraphSize()
        maxWeight, minWeight = self._model.maxMinWeight()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {nN} Numero di archi: {nE}"))
        self._view.txt_result.controls.append(ft.Text(f"Informazioni sui pesi degli archi - valore minimo: {minWeight} e valore massimo {maxWeight}"))
        self._view.update_page()
    def handle_countedges(self, e):
        try:
            soglia = int(self._view.txt_name.value)
        except ValueError:
            self._view.create_alert("Errore - la soglia inserita non è un intero")
            return

        archiMinori, archiMaggiori = self._model.contaArchi(soglia)
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia {archiMaggiori}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore della soglia {archiMinori}"))
        self._view.update_page()

    def handle_search(self, e):
        try:
            soglia = int(self._view.txt_name.value)
        except ValueError:
            self._view.create_alert("Errore - la soglia inserita non è un intero")
            return

        bestPath, cost = self._model.getBestPath(soglia)
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: {cost}"))
        for i in range(len(bestPath)-1):
            self._view.txt_result3.controls.append(ft.Text(f"{bestPath[i]} --> {bestPath[i+1]}: {self._model.getPesoArco(bestPath[i], bestPath[i+1])}"))

        self._view.update_page()