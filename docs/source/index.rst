.. Quality Nexus documentation master file, created by
   sphinx-quickstart on Thu Dec  5 09:56:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Quality Nexus documentation
===========================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Overview
--------
Quality Nexus is a project that helps predict various manufacturing specifications using machine learning models. It can be used for tasks such as predicting production cost and defect status based on input data. The tool aims to streamline decision-making in manufacturing environments by leveraging predictive analytics.

Installation
------------
To install **Quality Nexus**, you must have **Python 3.11**, **3.10**, or **3.9**. Follow the steps below:

1. Clone the repository:

```
git clone https://github.com/M-T-OUHADDA/Quality-Nexus.git cd Quality-Nexus
```

2. Create a virtual environment:

```
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```
  source venv/bin/activate
  ```

4. Install dependencies:

```
pip install -r requirements.txt
```


Usage
-----
There are three main ways to interact with **Quality Nexus**:

1. **Predicting a Single Value**:
- Use sliders and number inputs in the Streamlit interface to predict a single manufacturing specification (e.g., production cost or defect status).

2. **Editing a Whole DataFrame**:
- You can also edit a whole dataset in a DataFrame format to make multiple predictions based on your adjustments.

3. **Uploading a CSV**:
- Upload a CSV file containing your data, and **Quality Nexus** will process it to generate predictions for each row.


API Reference
-------------
Currently, **Quality Nexus** does not use an external API. It is deployed as a **Streamlit** application, and you can interact with it directly through the Streamlit interface.


Examples
--------
More examples of how to use the tool will be provided soon. Stay tuned!

Contributing
------------
If you would like to contribute to **Quality Nexus**, please follow these steps:

1. Fork the repository to your own GitHub account.
2. Create a new branch for your feature or bug fix:

```
git checkout -b feature-name
```

3. Make your changes and commit them:

```
git commit -am 'Add new feature'

```

4. Push your changes to your fork:

```
git push origin feature-name
```

5. Submit a pull request.

For any further questions or help, feel free to reach out through issues or contact.

FAQ
---
This section will be updated soon with frequently asked questions.