# tsgen : GAN-based Generation using STL-Robust Decomposed Time Series 
A tensorflow implementation of tsgen, an anomaly-preserving multi time series generation technique.
tsgen applies InfoGAN model ([https://arxiv.org/abs/1606.03657](https://arxiv.org/abs/1606.03657))
to time series data for classifying time series data through unsupervised way. To extract the best of time series 
features, tsgen decomposes the data using the STL-Robust decomposition.  



## Sample Data

Any csv formatted time series data as following can be used: 

<pre><code>
time,series1,series2 ... 
1,11.1,21.1 .. 
2,12.2,22.2 .. 
3,13.0,23.1 .. 
     .
     .
     .
</code></pre>

The file path should be put in the parameters files: *parameters.json*. 

#### IMPORTANT TO NOTE

As for now, tsgen supports only 1D Time series. 



## Dependencies

Python v.3.6.

## Build

Build all databases using the installation script located in the root folder

```bash
sh install_all_linux.sh
```


## Model parameters

The model parameters are stored in the **parameters.json** file. 

## Running tsgen

Execute 
<pre><code>
python main.py
</code></pre>
to run the tsgen pipeline, this will decompose the time series data using the STL-Robust decomposition,
train a model for each component, generate new time series data then reconstruct the time series data. 


## Generated time series data sample
 
After running the generation script, the output is: 

* *results/dataset/decomposition/*: the  STL-Robust decomposition result.
* *results/dataset/model/*: the learned models. trainResidue for example is the model built by learning from the Residue component, model/trainOri is the model built by learning from the original data. 
* *results/dataset/model/train{Ori, Trend, Seasonality, Residue}/fake.csv*: the generated data from the associated model as windows.
* *results/dataset/model/train{Ori, Trend, Seasonality, Residue}/fake_long.csv*: the generated data from the associated model as long time series that are constructed by merging windows.
* *results/dataset/generated_long_components.csv*: the generated data as long time series that are constructed by merging windows..
* *results/dataset/generated-components-summed.csv*: the generated data that sum the components windows.results/results_metrics.json: metrics on the generated data. 





## Other Ressources


1. [STL-Robust Decomposition](https://github.com/LeeDoYup/RobustSTL)
1. [Original GAN tensorflow implementation](https://github.com/buriburisuri/sugartensor/blob/master/sugartensor/example/mnist_gan.py)
1. [InfoGAN tensorflow implementation](https://github.com/buriburisuri/sugartensor/blob/master/sugartensor/example/mnist_info_gan.py)


