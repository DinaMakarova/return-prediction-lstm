def model_fn(params):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(params['lstm_size'], input_shape=(7, 6)))
    model.add(tf.keras.layers.Dropout(params['dropout']))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(
        optimizer = tf.keras.optimizers.Adam(params['learning_rate']), loss='binary_crossentropy', metrics=['accuracy'])
    callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)]
    history = model.fit_generator(
        train_generator, validation_data=val_generator, callbacks=callbacks, epochs=100, verbose=1).history
    return (history, model)



def random_search(model_fn, search_space, n_iter, search_dir):
    results = []
    os.mkdir(search_dir)
    best_model_path = os.path.join(search_dir, 'best_model.h5')
    results_path = os.path.join(search_dir, 'results.csv')
    
    for i in range(n_iter):
        params = {k: v[np.random.randint(len(v))] for k, v in search_space.items()}
        history, model = model_fn(params)
        epochs = np.argmax(history['val_accuracy']) + 1
        result = {k: v[epochs - 1] for k, v in history.items()}
        params['epochs'] = epochs
        if i == 0:
            best_val_acc = result['val_accuracy']
            model.save(best_model_path)
        if result['val_accuracy'] > best_val_acc:
            best_val_acc = result['val_accuracy']
            model.save(best_model_path)
            result = {**params, **result}
            results.append(result)
            tf.keras.backend.clear_session()
            print(f"iteration {i + 1} – {', '.join(f'{k}:{v:.4g}' for k, v in result.items())}")
    
    best_model = tf.keras.models.load_model(best_model_path)
    results = pd.DataFrame(results)
    results.to_csv(results_path)
    return (results, best_model, history)