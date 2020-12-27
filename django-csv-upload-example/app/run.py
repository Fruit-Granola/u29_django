import predict

trainer = predict.Trainer()
x_train, model = trainer.Process()

#print(x_train.info())
#print(type(model))

predictor = predict.Predictor("test_x.csv")
predictor.FitToTrain(x_train)
predictor.FillNa()
predictor.DataToArray()
predictor.Prediction(model)

result = predictor.ToSubmitFormat()
print(result)
predictor.ToCsv()
