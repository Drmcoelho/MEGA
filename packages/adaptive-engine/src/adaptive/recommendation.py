class RecommendationService:
    """
    Placeholder para futura lógica de recomendação:
    - Combinar itens 'due' do IntervalScheduler
    - Ordenar por menor mastery
    """

    def recommend(self, due_items, mastery_snapshot):
        return sorted(due_items, key=lambda x: mastery_snapshot.get(x, 0))
