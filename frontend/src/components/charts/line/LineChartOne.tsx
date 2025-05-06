import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

export default function LineChartOne() {
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
    <div className="max-w-full overflow-x-auto custom-scrollbar">
      <div id="chartEight" className="min-w-[1000px]">
        <Chart options={options} series={series} type="area" height={310} />
      </div>
    </div>
  );
}
