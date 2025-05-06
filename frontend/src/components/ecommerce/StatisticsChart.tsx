import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import ChartTab from "../common/ChartTab";

export default function StatisticsChart() {
  const options: ApexOptions = {
    legend: {
      show: false, // Masquer la légende
      position: "top",
      horizontalAlign: "left",
    },
    colors: ["#465FFF", "#9CB9FF"], // Définir les couleurs des lignes
    chart: {
      fontFamily: "Outfit, sans-serif",
      height: 310,
      type: "line", // Définir le type de graphique sur 'line'
      toolbar: {
        show: false, // Masquer la barre d'outils du graphique
      },
    },
    stroke: {
      curve: "straight", // Définir le style de ligne (droit, lisse ou en escalier)
      width: [2, 2], // Largeur des lignes pour chaque série de données
    },

    fill: {
      type: "gradient",
      gradient: {
        opacityFrom: 0.55,
        opacityTo: 0,
      },
    },
    markers: {
      size: 0, // Taille des points de repère
      strokeColors: "#fff", // Couleur de la bordure des points
      strokeWidth: 2,
      hover: {
        size: 6, // Taille des points au survol
      },
    },
    grid: {
      xaxis: {
        lines: {
          show: false, // Masquer les lignes de la grille sur l'axe x
        },
      },
      yaxis: {
        lines: {
          show: true, // Afficher les lignes de la grille sur l'axe y
        },
      },
    },
    dataLabels: {
      enabled: false, // Désactiver les étiquettes de données
    },
    tooltip: {
      enabled: true, // Activer les infobulles
      x: {
        format: "dd MMM yyyy", // Format pour les infobulles de l'axe x
      },
    },
    xaxis: {
      type: "category", // Axe x basé sur des catégories
      categories: [
        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Juin",
        "Juil",
        "Août",
        "Sep",
        "Oct",
        "Nov",
        "Déc",
      ],
      axisBorder: {
        show: false, // Masquer la bordure de l'axe x
      },
      axisTicks: {
        show: false, // Masquer les ticks de l'axe x
      },
      tooltip: {
        enabled: false, // Désactiver les infobulles pour les points de l'axe x
      },
    },
    yaxis: {
      labels: {
        style: {
          fontSize: "12px", // Ajuster la taille de la police pour les étiquettes de l'axe y
          colors: ["#6B7280"], // Couleur des étiquettes
        },
      },
      title: {
        text: "", // Supprimer le titre de l'axe y
        style: {
          fontSize: "0px",
        },
      },
    },
  };

  const series = [
    {
      name: "Ventes",
      data: [180, 190, 170, 160, 175, 165, 170, 205, 230, 210, 240, 235],
    },
    {
      name: "Revenu",
      data: [40, 30, 50, 40, 55, 40, 70, 100, 110, 120, 150, 140],
    },
  ];
  return (
    <div className="rounded-2xl border border-gray-200 bg-white px-5 pb-5 pt-5 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6">
      <div className="flex flex-col gap-5 mb-6 sm:flex-row sm:justify-between">
        <div className="w-full">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Statistiques
          </h3>
          <p className="mt-1 text-gray-500 text-theme-sm dark:text-gray-400">
            Objectif que vous avez défini pour chaque mois
          </p>
        </div>
        <div className="flex items-start w-full gap-3 sm:justify-end">
          <ChartTab />
        </div>
      </div>

      <div className="max-w-full overflow-x-auto custom-scrollbar">
        <div className="min-w-[1000px] xl:min-w-full">
          <Chart options={options} series={series} type="area" height={310} />
        </div>
      </div>
    </div>
  );
}
