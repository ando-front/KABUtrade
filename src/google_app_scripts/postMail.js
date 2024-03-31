function doGet(e) {
  return ContentService.createTextOutput(
    "This app only accepts POST requests."
  );
}

// この関数はHTTP POSTリクエストを受け取り、そのリクエストのパラメータに含まれる`signalType`に応じて、異なるメールを送信します。この関数をGASのウェブアプリケーションとしてデプロイし、得られたエンドポイントURLに対して適切な`signalType`パラメータ（`buy`または`sell`）を含むPOSTリクエストを送信することで、メールの自動送信が行われます。
function doPost(e) {
  // リクエストから信号の種類とシグナルの詳細を取得
  var signalType = e.parameter.signalType;
  var signalKind = e.parameter.signalKind;
  var subject = "";
  var message = "";

  // 信号の種類に応じて件名と本文を設定
  if (signalType === "Buy") {
    subject = "買いシグナルの通知";
    message =
      "賢二さん、SP500の買いシグナル（" +
      signalKind +
      "）が出ましたので、買い注文を入れてください。";
  } else if (signalType === "Sell") {
    subject = "売りシグナルの通知";
    message =
      "賢二さん、SP500の売りシグナル（" +
      signalKind +
      "）が出ましたので、売り注文を入れてください。";
  } else {
    // 不明な信号の種類の場合
    subject = "買いor売りシグナルはありませんでした";
    message = "本日は買いor売りシグナルはありませんでした";
  }

  // メール送信
  MailApp.sendEmail({
    to: "angie07.inet@gmail.com",
    subject: subject,
    body: message,
  });

  // 正常終了のレスポンスを返す
  return ContentService.createTextOutput("Email sent.");
}
