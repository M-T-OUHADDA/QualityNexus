Usage
=====

There are **three** primary ways to interact with **Quality Nexus**:

1. **Predicting a Single Value**:

   - Use the Streamlit interface with sliders and input fields to predict a specific manufacturing specification (e.g., production cost or defect status).

2. **Editing a Whole DataFrame**:

   - Modify an entire dataset in a DataFrame format and make multiple predictions based on your adjustments.

3. **Uploading a CSV**:

   - Upload a CSV file containing data, and **Quality Nexus** will process it and generate predictions for each row.

The application ensures a seamless and efficient process for generating predictions tailored to your specifications. Here's how it works:

1. **Select Specifications**:

    - Begin by choosing the desired specifications from the left sidebar. This step automatically selects the best-trained model for your requirements, guaranteeing optimal results.

2. **Input Data and Choose Additional Features**:

    - Enter your dataset and configure any additional features or parameters necessary for your prediction.

3. **Generate Predictions**:

    - Click on :kbd:`Get Prediction` to calculate the desired result or refresh if modifications or adjustments are made to apply the latest changes and generate updated predictions.

    .. tip::

        If selecting overlayed graphs try to change colors for more accessibility

4. **Save Your Work**:

    - Easily save the DataFrame along with its predictions locally by clicking on download icon. This ensures your work is preserved for future reference or analysis.

This streamlined workflow allows for precise predictions while maintaining flexibility for iterative adjustments, making it user-friendly.

Examples
--------

Illustration of using our tool:

We will walk you through the steps to use the tool that allows you to upload data, choose prediction features, visualize the data, and edit it on the fly. Let’s see how it works!

1. **Make a One-Value Prediction**:

    - In the Select Features for Prediction section, you'll see a **Selector** with all available parameters that might be predicted.

        .. image:: _static/side_input_edit.png
           :align: center


    - In the Enter Value for Prediction section, you'll see many input field. Fill them with your data

    - Click the Predict button, and the system will output the predicted target value based on the model.


        .. image:: _static/input_edit_test.png
           :align: center

2. **Upload Your Data**:

    - Select Input Form as Data Upload:

        .. image:: _static/side_data_upload.png
           :align: center

    - Click :kbd:`Browse files` or **Drag** the desired file.

    - Select a **CSV** file from your local machine that contains the data you want to analyze.

    - Once the file is uploaded, you’ll see a preview of your data, including the number of rows and columns.

        .. image:: _static/data_upload_test.png
           :align: center

    - Click :kbd:`Get Prediction`:

        .. image:: _static/data_upload_test2.png
           :align: center

3. **Data Aggregation and Visualizations**:

You can also analyze aggregated features in your dataset for more insights. The Aggregated Features section will display a frame that shows the sum, average...

    .. image:: _static/agg.png
       :align: center

    .. image:: _static/agg2.png
       :align: center

4. **Interactive Plots and Heatmaps**:

The application provides interactive visualizations to help you gain more insights from your data. The Interactive Plots section allows you to explore various types of visualizations, like bar charts, scatter plots, and line charts.

    .. image:: _static/visua.png
       :align: center


You can hover over data points, zoom in, and filter the plots to understand the relationships between features more clearly.

    .. image:: _static/line_plot.png
       :align: center


The Heatmap will show you the correlation matrix of your data, helping you see which features have strong relationships with others.

    .. image:: _static/heatmap.png
       :align: center

5. **Editing the Data Frame**:

If you need to edit a dataset, the application allows you to a streamlit data editor.

    - In the Edit Data Frame section, you can directly modify the values in your dataset.

        .. image:: _static/side_data_frame.png
           :align: center

        .. image:: _static/data_editor.png
           :align: center

    - Make instant changes, such as correcting an incorrect value or adding new rows.

    - Once you're done editing, click the :kbd:`Get Prediction` or use data editor tools to save a copy.
        .. image:: _static/tools.png
           :align: center
