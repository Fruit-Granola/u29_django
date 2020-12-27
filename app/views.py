import csv
import io

from django.http import HttpResponse
from django.views.generic import FormView

from .forms import UploadForm
from .predict import Trainer, Predictor


# Create your views here.
class UploadView(FormView):
    form_class = UploadForm
    template_name = 'app/UploadForm.html'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']

        # 入力データから予測を立てる
        trainer = Trainer()
        x_train, model = trainer.Process()

        predictor = Predictor(csvfile)
        predictor.FitToTrain(x_train)
        predictor.FillNa()
        predictor.DataToArray()
        predictor.Prediction(model)

        # 結果をcsvファイルでダウンロード
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename = "prediction.csv"'
        writer = csv.writer(response)
        writer.writerow(['お仕事No.', '応募数 合計'])
        for row in predictor.ToSubmitFormat().values:
            writer.writerow(row)
        return response
