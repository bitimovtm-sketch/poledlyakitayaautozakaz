<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Настройка поля</title>
  <script src="//api.bitrix24.com/api/v1/"></script>
</head>
<body style="font-family: sans-serif; padding: 20px; line-height: 1.6;">
  <h3>Настройка поля «Форматированный текст»</h3>
  <div id="status"></div>

  <script>
    var USER_TYPE_ID = 'richtext';
    var HANDLER_URL = window.location.origin + '/field';

    function log(text) {
      document.getElementById('status').innerHTML += '<div>' + text + '</div>';
    }

    function safeError(result) {
      var err = result.error();
      if (err && typeof err.ex === 'object' && err.ex !== null) {
        return (err.ex.error || '') + ': ' + (err.ex.error_description || '');
      }
      try { return JSON.stringify(err); } catch (e) { return String(err); }
    }

    BX24.init(function () {
      // Шаг 1: проверяем установку — по чек-листу Bitrix24 INSTALLED должен быть true
      BX24.callMethod('app.info', {}, function (appInfoResult) {
        if (appInfoResult.error()) {
          log('Ошибка app.info: ' + safeError(appInfoResult));
          return;
        }
        var appInfo = appInfoResult.data();
        var appId = appInfo.ID;
        log('APP ID = ' + appId + ', INSTALLED = ' + appInfo.INSTALLED);

        if (String(appInfo.INSTALLED) !== 'true' && appInfo.INSTALLED !== true) {
          log('Приложение ещё не установлено до конца. Закрой это окно и открой приложение заново ' +
              '(или нажми «Переустановить» в настройках приложения).');
          return;
        }

        // Шаг 2: регистрируем тип поля (повторная регистрация даст ошибку — это нормально)
        BX24.callMethod('userfieldtype.add', {
          USER_TYPE_ID: USER_TYPE_ID,
          HANDLER: HANDLER_URL,
          TITLE: 'Форматированный текст',
          DESCRIPTION: 'Текст с сохранением абзацев и форматирования'
        }, function (typeResult) {
          if (typeResult.error()) {
            log('userfieldtype.add: ' + safeError(typeResult) + ' — если тип уже есть, это не страшно.');
          } else {
            log('Тип поля зарегистрирован.');
          }

          // Шаг 3: подтверждаем регистрацию типа
          BX24.callMethod('userfieldtype.list', {}, function (listResult) {
            if (listResult.error()) {
              log('Ошибка userfieldtype.list: ' + safeError(listResult));
              return;
            }
            var types = listResult.data() || [];
            var found = types.some(function (t) { return t.USER_TYPE_ID === USER_TYPE_ID; });
            if (!found) {
              log('Тип "' + USER_TYPE_ID + '" не найден. Зарегистрированные типы: ' + JSON.stringify(types));
              return;
            }
            log('Тип "' + USER_TYPE_ID + '" подтверждён.');

            var fullTypeId = 'rest_' + appId + '_' + USER_TYPE_ID;

            // Шаг 4: создаём поле на сделках
            BX24.callMethod('crm.deal.userfield.add', {
              fields: {
                LABEL: 'Описание (форматированное)',
                FIELD_NAME: 'RICH_DESCRIPTION',
                USER_TYPE_ID: fullTypeId,
                MULTIPLE: 'N',
                MANDATORY: 'N'
              }
            }, function (fieldResult) {
              if (fieldResult.error()) {
                log('crm.deal.userfield.add: ' + safeError(fieldResult) + ' — если поле уже создано, это не страшно.');
              } else {
                log('<b>Готово! Поле создано. Код поля: UF_CRM_RICH_DESCRIPTION</b>');
              }

              // Шаг 5: показываем точный код поля из списка
              BX24.callMethod('crm.deal.userfield.list', {
                filter: { FIELD_NAME: 'UF_CRM_RICH_DESCRIPTION' }
              }, function (ufListResult) {
                if (!ufListResult.error()) {
                  var items = ufListResult.data() || [];
                  if (items.length > 0) {
                    log('<b>Код поля для Railway (FIELD_CODE): ' + items[0].FIELD_NAME + '</b>');
                  }
                }
              });
            });
          });
        });
      });
    });
  </script>
</body>
</html>
