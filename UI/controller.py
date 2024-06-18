import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        distanza=self._view._txtDistanza.value
        if distanza=="":
            self._view.create_alert("INSERIRE UNA DISTANZA")
            return
        prov=self._view._ddProvider.value
        if prov is None:
            self._view.create_alert("SELEZIONARE UN PROVIDER")
            return
        grafo = self._model.creaGrafo(float(distanza), prov)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))

        for nodi in grafo.nodes:
            self._view._ddTarget.options.append(ft.dropdown.Option(
                text=nodi))
        self._view.update_page()



    def handleAnalisiGrafo(self, e):
        analisiR,peso=self._model.analisi()
        self._view.txt_result.controls.append(ft.Text("VERTICI CON PIU' VICINI"))
        for nodo in analisiR:
            self._view.txt_result.controls.append(ft.Text(f"{nodo}, #vicini={peso}"))
        self._view.update_page()


    def handleCalcolaPercorso(self, e):
        str = self._view._txtStringa.value
        if str=="":
            self._view.create_alert("INSERIRE UNA STRINGA")
            return
        target=self._view._ddTarget.value
        if target is None:
            self._view.create_alert("SELEZIONARE UN TARGET")
            return

        soluzione,peso=self._model.getBestPath(target,str)
        self._view.txt_result.controls.append(ft.Text(f"Il percorso selezionato tocca {peso} località:"))
        for nodo in soluzione:
            self._view.txt_result.controls.append(ft.Text(f"{nodo}"))
        self._view.update_page()

    def fillDD(self):
        provider=self._model.provider
        for prov in provider:
            self._view._ddProvider.options.append(ft.dropdown.Option(
                text=prov))

