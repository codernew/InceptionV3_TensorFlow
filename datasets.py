# encoding: utf-8

import tensorflow as tf
import settings
FLAGS = settings.FLAGS


class DataSet:
    def __init__(self):
        pass

    def _generate_image_and_label_batch(self, image, label, min_queue_examples, batch_size):
        '''
        imageとlabelのmini batchを生成
        '''
        num_preprocess_threads = FLAGS.num_threads
        images, labels = tf.train.shuffle_batch(
            [image, label],
            batch_size=batch_size,
            num_threads=num_preprocess_threads,
            capacity=min_queue_examples + 3 * FLAGS.batch_size,
            min_after_dequeue=min_queue_examples
        )

        # Display the training images in the visualizer
        #tf.image_summary('images', images, max_images=BATCH_SIZE)
        return images, labels

    def csv_inputs(self, csv, batch_size):
        print("input csv file path: %s" % (csv))
        filename_queue = tf.train.string_input_producer([csv], shuffle=True)
        reader = tf.TextLineReader()
        _, serialized_example = reader.read(filename_queue)
        filename, label = tf.decode_csv(serialized_example, [["path"], [0]])

        png = tf.read_file(filename)
        image = tf.image.decode_png(png, channels=3)
        image = tf.cast(image, tf.float32)
        #image.set_shape([IMAGE_HEIGHT_ORG, IMAGE_WIDTH_ORG, IMAGE_DEPTH_ORG])
        image = tf.image.resize_images(image, FLAGS.input_h, FLAGS.input_w)

        min_fraction_of_examples_in_queue = 0.4
        min_queue_examples = int(100 * min_fraction_of_examples_in_queue)
        print ('filling queue with %d train images before starting to train.  This will take a few minutes.' % min_queue_examples)

        return self._generate_image_and_label_batch(image, label, min_queue_examples, batch_size)