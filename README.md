

# **VisualAI: A Generative AI Healthcare Solution**

## **<u>Our Sector:</u>**
- Healthcare
- Web Development
- AI & Machine Learning

## **Hackathon Overview**

As part of the NVIDIA AI Workbench hackathon, we developed **VisualAI**, a generative AI platform aimed at revolutionizing healthcare diagnostics and consultations. Utilizing the capabilities of NVIDIA AI Workbench, we focused on enhancing developer productivity in data science and machine learning tasks.

## **What Inspired Us**

Every year, diagnostic errors account for approximately 10% of patient deaths globally, with around **2.6 million deaths** occurring in low- and middle-income countries. These challenges are exacerbated by a lack of access to experienced healthcare professionals.

Our motivation stems from personal experiences, particularly witnessing a relative in Bangladesh struggle to access timely and effective healthcare. This experience illuminated the systemic barriers within healthcare, including costly travel, limited specialist availability, and the risk of losing critical medical reports.

We aim to **create a platform that securely stores medical reports, provides real-time access**, and allows doctors and patients to collaboratively analyze and discuss these reports during consultations, ultimately **reducing diagnostic errors** and improving healthcare access globally.

## **What It Does**

VisualAI harnesses generative AI to transform healthcare management by streamlining medical report processing and facilitating remote consultations.

### Key Features:
1. **Generative Report Processing & Visualization:**
   - **Automatic Data Extraction**: Utilizes advanced OCR to extract essential details from medical reports.
   - **Dynamic Data Organization**: Structures and organizes data for efficient access.
   - **Visual Data Insights**: Converts data into interactive graphs, metrics, and tables for enhanced understanding.

2. **AI-Enhanced Recommendations:**
   - **Symptom-Based Specialist Suggestions**: Employs generative AI to recommend specialists based on patient symptoms.

3. **Real-Time Video Consultations:**
   - **Integrated Video Calls**: Allows patients and doctors to view and discuss visualized data during consultations.

4. **Secure and Continuous Data Tracking:**
   - **Robust Data Storage**: Medical reports are securely stored for reliable historical data access.

5. **Global Accessibility:**
   - Connects patients with specialists worldwide through video consultations, overcoming geographical barriers.

## **How We Built It**

Leveraging the power of NVIDIA AI Workbench, we developed VisualAI with a focus on generative AI technologies:

- **OCR Technology**: Integrated Asprise OCR API for accurate text extraction from reports, achieving a confidence rate of 96.5%.
- **Data Cleaning & Structuring**: Used Google Gemini for data cleaning and structuring, converting raw data into JSON for easy access.
- **Generative AI for Recommendations**: Implemented NLP and machine learning with scikit-learn and NLTK for intelligent doctor recommendations based on symptoms.
- **Responsive Frontend**: Developed a user-friendly interface using Django Templating Engine, JavaScript, and CSS.
- **Real-Time Video Chat**: Integrated ZEGOCLOUD for seamless video consultation functionality.

## **Technologies Used**
- **Backend**: Django, Python, Django Rest Framework
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: Asprise OCR, Google Gemini, ZEGOCLOUD
- **Data Science**: NLTK, Scikit-learn
- **Generative AI**: NVIDIA AI Workbench
- **Database**: MySQL

## **Challenges We Faced**

1. **OCR Integration**: We initially encountered difficulties with OCR accuracy, resolved by adopting Asprise OCR API.
2. **Video Call Integration**: Faced challenges with Zoom integration, which we overcame by using ZEGOCLOUD.

## **Accomplishments We’re Proud Of**
- Achieving an OCR accuracy of over 96%.
- Successfully integrating real-time video functionality with comprehensive data visualization.
- Creating a platform that demonstrates the potential of generative AI in enhancing healthcare delivery.

## **What We Learned**
Through this project, we deepened our understanding of generative AI applications, API integrations, and advanced NLP techniques. We improved our project management and collaboration skills while coordinating various technologies to deliver a cohesive solution.

## **What's Next**

Our future plans include:
1. **AI-Powered Diagnostic Models**: Developing models for disease detection using TensorFlow and PyTorch.
2. **3D Visualization from 2D X-Rays**: Utilizing NVIDIA Clara and 3D Slicer to enhance diagnostic accuracy through 3D modeling.
3. **Hospital Integration**: Implementing RESTful APIs for seamless integration with hospital systems.
4. **Sustainability Initiatives**: Promoting reduced paper usage to foster environmental and financial sustainability.

### Overview of NVIDIA AI

NVIDIA is a leader in AI and deep learning technologies, providing a robust platform that accelerates AI applications across various industries. Their offerings include powerful GPUs, software frameworks, and specialized tools that enable developers to build, train, and deploy AI models efficiently.

### Key Technologies

1. **NVIDIA GPUs**:
   - NVIDIA's Graphics Processing Units (GPUs) are designed for parallel processing, making them ideal for training complex deep learning models. The architecture of NVIDIA GPUs allows for high throughput, which significantly reduces the time required to train models.

2. **CUDA**:
   - Compute Unified Device Architecture (CUDA) is a parallel computing platform and programming model that enables developers to leverage the GPU's power for general-purpose computing. CUDA allows for faster computations in AI, making it easier to develop applications in various fields, including healthcare.

3. **NVIDIA AI Workbench**:
   - NVIDIA AI Workbench is a development environment that simplifies the creation of generative AI applications. It provides tools and resources to quickly get up and running with AI workflows, allowing developers to focus on building innovative solutions without being bogged down by setup complexities.

4. **NVIDIA Clara**:
   - Clara is a platform specifically designed for healthcare. It provides a suite of AI tools and pre-trained models for medical imaging, genomics, and drug discovery. Clara can transform 2D medical images into 3D models, improving diagnostic accuracy and enabling better visualization for healthcare professionals.

5. **TensorRT**:
   - TensorRT is a high-performance deep learning inference optimizer and runtime. It allows developers to deploy trained models efficiently, ensuring they run quickly and effectively on NVIDIA GPUs. This is particularly important in real-time applications, such as healthcare diagnostics and automated imaging analysis.

### Applications in Healthcare

1. **Medical Imaging**:
   - NVIDIA's AI technologies are widely used in medical imaging to enhance image quality, automate diagnosis, and reduce analysis time. For example, deep learning algorithms can analyze X-rays, MRIs, and CT scans to identify anomalies, leading to quicker and more accurate diagnoses.

2. **Predictive Analytics**:
   - AI can analyze vast amounts of patient data to identify patterns and predict outcomes. This is particularly useful in personalized medicine, where treatment plans can be tailored to individual patients based on predictive models.

3. **Natural Language Processing (NLP)**:
   - NVIDIA's technologies enable the processing of unstructured data, such as clinical notes and patient histories. NLP can extract meaningful insights from this data, aiding in clinical decision-making and improving patient care.

4. **Telemedicine**:
   - With the rise of telemedicine, NVIDIA's AI tools facilitate real-time video consultations, allowing healthcare providers to connect with patients remotely. AI can enhance these interactions by providing real-time data analysis and insights during consultations.

### Conclusion

NVIDIA AI technologies offer transformative capabilities that drive innovation in healthcare and other fields. By leveraging powerful GPUs, specialized software, and AI frameworks, developers can create solutions that improve patient outcomes, streamline workflows, and enhance the overall efficiency of healthcare systems. As the demand for AI in healthcare continues to grow, NVIDIA remains at the forefront, providing the tools necessary to meet these challenges head-on. 

