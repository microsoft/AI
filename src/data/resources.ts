import { BookOpen, Code2, Layers, Cpu, Database, Cloud, Terminal, BrainCircuit } from 'lucide-react';

export interface ResourceItem {
  id: string;
  title: string;
  description: string;
  url: string;
  tags: string[];
  icon?: any;
}

export interface ResourceCategory {
  id: string;
  title: string;
  description: string;
  items: ResourceItem[];
}

export const resources: ResourceCategory[] = [
  {
    id: 'ai100',
    title: 'AI100 - Samples',
    description: 'A collection of open source Python repositories created by Microsoft product teams focusing on AI services.',
    items: [
      {
        id: 'azure-ml-sdk',
        title: 'Azure ML Python SDK',
        description: 'Python notebooks with ML and deep learning examples with Azure Machine Learning.',
        url: 'https://github.com/Azure/MachineLearningNotebooks',
        tags: ['Python', 'Azure ML', 'Notebooks'],
        icon: Code2
      },
      {
        id: 'cognitive-services',
        title: 'Azure Cognitive Services Python SDK',
        description: 'Learn how to use the Cognitive Services Python SDK with these samples.',
        url: 'https://github.com/Azure-Samples/cognitive-services-python-sdk-samples',
        tags: ['Python', 'Cognitive Services', 'SDK'],
        icon: BrainCircuit
      },
      {
        id: 'intelligent-kiosk',
        title: 'Azure Intelligent Kiosk',
        description: 'Demos showcasing workflows and experiences built on top of Microsoft Cognitive Services.',
        url: 'https://github.com/microsoft/Cognitive-Samples-IntelligentKiosk',
        tags: ['Demos', 'Workflows', 'Cognitive Services'],
        icon: Layers
      },
      {
        id: 'mml-spark',
        title: 'MML Spark Samples',
        description: 'Ecosystem of tools aimed towards expanding the distributed computing framework Apache Spark.',
        url: 'https://github.com/Azure/mmlspark/tree/master/notebooks/samples',
        tags: ['Spark', 'Distributed Computing', 'MMLSpark'],
        icon: Database
      },
      {
        id: 'seismic-dl',
        title: 'Seismic Deep Learning Samples',
        description: 'Deep Learning for Seismic Imaging and Interpretation.',
        url: 'https://github.com/microsoft/seismic-deeplearning/',
        tags: ['Deep Learning', 'Seismic', 'Imaging'],
        icon: ActivityIcon
      }
    ]
  },
  {
    id: 'ai200',
    title: 'AI200 - Reference Architectures',
    description: 'Architectures arranged by scenario, including considerations for scalability, availability, manageability, and security.',
    items: [
      {
        id: 'classic-ml-k8s',
        title: 'Deploy Classic ML Model on Kubernetes',
        description: 'Train LightGBM model locally using Azure ML, deploy on Kubernetes or IoT Edge for real-time scoring.',
        url: 'https://github.com/microsoft/MLAKSDeployAML',
        tags: ['Python', 'CPU', 'Real-Time Scoring', 'Kubernetes'],
        icon: Cloud
      },
      {
        id: 'dl-k8s',
        title: 'Deploy Deep Learning Model on Kubernetes',
        description: 'Deploy image classification model on Kubernetes or IoT Edge for real-time scoring using Azure ML.',
        url: 'https://github.com/microsoft/AKSDeploymentTutorialAML',
        tags: ['Python', 'Keras', 'Real-Time Scoring', 'Kubernetes'],
        icon: Cloud
      },
      {
        id: 'hyperparameter',
        title: 'Hyperparameter Tuning',
        description: 'Train LightGBM model locally and run Hyperparameter tuning using Hyperdrive in Azure ML.',
        url: 'https://github.com/Microsoft/MLHyperparameterTuning',
        tags: ['Python', 'CPU', 'Training', 'Hyperdrive'],
        icon: Cpu
      },
      {
        id: 'dl-pipelines',
        title: 'Deploy Deep Learning Model on Pipelines',
        description: 'Deploy PyTorch style transfer model for batch scoring using Azure ML Pipelines.',
        url: 'https://github.com/Azure/Batch-Scoring-Deep-Learning-Models-With-AML',
        tags: ['Python', 'GPU', 'Batch Scoring', 'PyTorch'],
        icon: Layers
      },
      {
        id: 'classic-ml-pipelines',
        title: 'Deploy Classic ML Model on Pipelines',
        description: 'Deploy one-class SVM for batch scoring anomaly detection using Azure ML Pipelines.',
        url: 'https://github.com/Microsoft/AMLBatchScoringPipeline',
        tags: ['Python', 'CPU', 'Batch Scoring', 'SVM'],
        icon: Layers
      },
      {
        id: 'r-ml-k8s',
        title: 'Deploy R ML Model on Kubernetes',
        description: 'Deploy ML model for real-time scoring on Kubernetes.',
        url: 'https://github.com/Azure/RealtimeRDeployment',
        tags: ['R', 'CPU', 'Real-Time Scoring', 'Kubernetes'],
        icon: Terminal
      },
      {
        id: 'spark-databricks',
        title: 'Deploy Spark ML Model on Databricks',
        description: 'Deploy a classification model for batch scoring using Databricks.',
        url: 'https://github.com/Azure/BatchSparkScoringPredictiveMaintenance',
        tags: ['Python', 'Spark', 'Batch Scoring', 'Databricks'],
        icon: Database
      }
    ]
  },
  {
    id: 'ai300',
    title: 'AI300 - Best Practices',
    description: 'Best practices arranged by topic, including open source methods and considerations for production.',
    items: [
      {
        id: 'cv',
        title: 'Computer Vision',
        description: 'Accelerate the development of computer vision applications with examples and guidelines.',
        url: 'https://github.com/microsoft/computervision',
        tags: ['Computer Vision', 'Best Practices'],
        icon: BookOpen
      },
      {
        id: 'nlp',
        title: 'Natural Language Processing',
        description: 'State-of-the-art methods and common scenarios for text and language problems.',
        url: 'https://github.com/microsoft/nlp',
        tags: ['NLP', 'Text', 'Language'],
        icon: BookOpen
      },
      {
        id: 'recommenders',
        title: 'Recommenders',
        description: 'Examples and best practices for building recommendation systems (Jupyter notebooks).',
        url: 'https://github.com/microsoft/recommenders',
        tags: ['Recommenders', 'Jupyter'],
        icon: BookOpen
      },
      {
        id: 'mlops',
        title: 'MLOps',
        description: 'MLOps empowers data scientists and app developers to help bring ML models to production.',
        url: 'https://github.com/microsoft/MLOps',
        tags: ['MLOps', 'Production', 'DevOps'],
        icon: BookOpen
      }
    ]
  }
];

// Helper component for icon fallback
function ActivityIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  );
}
