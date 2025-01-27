
# **Druid Compression Reproduction Tutorial**

## **Introduction**
This tutorial demonstrates how to load datasets into **Druid** for the Compression Performance Workload [Figure 10]. Ensure all prerequisites are met before proceeding.

---

## **Prerequisites**
1. Linux/Ubuntu environment 24.
2. Druid and InfluxDB installed.
3. Switch to the virtual environment:

   ```bash
   source TSMvenv/bin/activate
   ```

---

## **Druid Setup**

### **1. Start Druid**
   ```bash
   cd systems/druid/
   sh install.sh; sh launch.sh # OR ./apache-druid-25.0.0/bin/start-single-server-medium
   ```
   This launches instances of Zookeeper and Druid services:

   ![image](https://github.com/user-attachments/assets/41b8fc45-7042-4aec-a9d5-c940fb2441b4)

---

### **2. Open the Web Console**
   After starting the Druid services, open the web console at:
   ```http://localhost:8888```
   It may take a few seconds for all Druid services to finish starting.

   ![image](https://github.com/user-attachments/assets/8b37a896-2c88-4098-8b74-9ef89ff7101a)

---

### **3. Load Synthetic Datasets**
   1. In the **Load Data** view, click **Connect external data**.
   2. Select the **Local disk** tile and enter the following values:
      - **Base directory**: `$ABSOLUTE_PATH/TSM-Bench/compression/datasets/`
      - **File filter**: the name of the file to load, for example: `outliers_2.csv`

---

### **4. Connect Data**
   Click **Connect Data** to proceed.

---

### **5. Parse Data**
   On the **Parse** page, you can examine the raw data and optionally:
   - Expand a row to see the corresponding source data.
   - Customize how the data is handled by selecting from the **Input format** options.
   - Adjust the primary timestamp column for the data. Druid requires data to have a primary timestamp column (stored internally as `__time`).

   ![image](https://github.com/user-attachments/assets/497e1597-4901-4444-9ab5-4065b36a28cd)

---

### **6. Configure Dataset Schema**
   Click **Next**. You’re given a schema to configure the dataset, secondary indices, and partitioning size. For reproducibility, use the default parameters.

   ![image](https://github.com/user-attachments/assets/5039bea2-939b-4e7e-aa08-be3d945eff1c)

---

### **7. Start Loading Data**
   Click **Start Loading Data**. You will be returned to the Query view, which displays the newly generated query. This query inserts the sample data into the table named `outlier_2.csv`, and the loading will begin.

   ![image](https://github.com/user-attachments/assets/54ade6da-144a-4017-8246-b0708a224918)

---

### **8. Monitor Ingestion**
   Click **Go to ingestion view** and wait until the task is finished:

   ![image](https://github.com/user-attachments/assets/31057088-bca6-45c0-b53e-828a91fa77e1)

---

### **9. Visualize Compression Size**
   To visualize the dataset compression size:
   - Go to **Datasources**.
   - You will find all loaded datasets and their size readings.

   ![image](https://github.com/user-attachments/assets/a9e0c219-504b-44c5-a469-4023fe94a147)

---

### **10. Repeat for Other Datasets**
   Repeat Step 3 for every synthetic dataset to be evaluated for the different dataset variations.

