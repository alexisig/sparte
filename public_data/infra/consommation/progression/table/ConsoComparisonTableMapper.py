from django.template.loader import render_to_string

from public_data.domain.consommation.progression.ConsommationProgression import (
    ConsommationProgressionLand,
)


class ConsoComparisonMapper:
    @staticmethod
    def map(consommation_progression: list[ConsommationProgressionLand]):
        first_land_consommation = consommation_progression[0] if consommation_progression else None

        if not first_land_consommation:
            raise ValueError("No consommation progression found")

        land_type_label = first_land_consommation.land.land_type_label

        headers = [land_type_label] + [str(conso.year) for conso in first_land_consommation.consommation] + ["Total"]

        data = [
            [land_conso.land.name]
            + [round(annual_conso.total, 2) for annual_conso in land_conso.consommation]
            + [round(land_conso.total_conso_over_period, 2)]
            for land_conso in consommation_progression
        ]

        return render_to_string(
            "public_data/partials/conso_comparison_table.html",
            {
                "headers": headers,
                "data": data,
            },
        )
