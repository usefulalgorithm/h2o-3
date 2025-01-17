from __future__ import division
from __future__ import print_function
from past.utils import old_div
import sys
sys.path.insert(1,"../../../")
import h2o
from tests import pyunit_utils
import pandas as pd
import zipfile
import statsmodels.api as sm
from h2o.estimators.glm import H2OGeneralizedLinearEstimator

def link_functions_binomial():
  print("Read in prostate data.")
  h2o_data = h2o.import_file(path=pyunit_utils.locate("smalldata/prostate/prostate_complete.csv.zip"))
  h2o_data.head()

  sm_data = pd.read_csv(zipfile.ZipFile(pyunit_utils.locate("smalldata/prostate/prostate_complete.csv.zip")).open("prostate_complete.csv")).values
  sm_data_response = sm_data[:,2]
  sm_data_features = sm_data[:,[1,3,4,5,6,7,8,9]]

  print("Testing for family: BINOMIAL")
  print("Set variables for h2o.")
  myY = "CAPSULE"
  myX = ["ID","AGE","RACE","GLEASON","DCAPS","PSA","VOL","DPROS"]

  print("Create models with canonical link: LOGIT")

  h2o_data[myY] = h2o_data[myY].asfactor()
  h2o_model = H2OGeneralizedLinearEstimator(family="binomial", link="logit",alpha=0.5, Lambda=0)
  h2o_model.train(x=myX, y=myY, training_frame=h2o_data)
  sm_model = sm.GLM(endog=sm_data_response, exog=sm_data_features, family=sm.families.Binomial(sm.families.links.logit())).fit()

  print("Compare model deviances for link function logit")
  h2o_deviance = old_div(h2o_model.residual_deviance(), h2o_model.null_deviance())
  sm_deviance = old_div(sm_model.deviance, sm_model.null_deviance)
  assert h2o_deviance - sm_deviance < 0.01, "expected h2o to have an equivalent or better deviance measures"



if __name__ == "__main__":
  pyunit_utils.standalone_test(link_functions_binomial)
else:
  link_functions_binomial()
