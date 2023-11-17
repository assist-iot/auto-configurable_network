import tensorflow as tf

# na koncu uczenia w run_ray trzeba dorzucic agent.export_policy_model("tf_model8")
# mnie zadzialalo z ray 2.0.0, ale trzeba bylo m.in. usunac linie steps += output["timesteps_this_iter"] w run_ray 

new_model = tf.saved_model.load('tf_model')
f = new_model.signatures["serving_default"]

# pierwsza tablica [1.,0.,0.5,0.0] to obserwacje, reszta nie jest chyba istotna
print(f(observations=tf.constant([[1.,0.,0.5,0.0]]),is_training=tf.constant(False),timestep=tf.constant(0,dtype=tf.int64),prev_reward=tf.constant(1.),prev_action=tf.constant(0,dtype=tf.int64)))
print(f(observations=tf.constant([[1.,0.,0.5,0.5]]),is_training=tf.constant(False),timestep=tf.constant(0,dtype=tf.int64),prev_reward=tf.constant(1.),prev_action=tf.constant(0,dtype=tf.int64))['q_values'])
print(f(observations=tf.constant([[0.,1.,0.5,0.5]]),is_training=tf.constant(False),timestep=tf.constant(0,dtype=tf.int64),prev_reward=tf.constant(1.),prev_action=tf.constant(0,dtype=tf.int64))['q_values'])
# w wyniku na moj gust istotne sa q_values; jezeli pierwsza wieksza to zwracamy akcje 0, jezeli druga to zwracamy 1
