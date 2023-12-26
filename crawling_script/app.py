from flask import Flask, jsonify, request
import feature_extractor as extractor

app = Flask(__name__)

import signal

class TimedOutExc(Exception):
    pass


def deadline(timeout, *args):
    def decorate(f):
        def handler(signum, frame):
            raise TimedOutExc()

        def new_f(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)
            result = f(*args)
            signal.alarm(0)
            return result

        new_f.__name__ = f.__name__
        return new_f
    return decorate


def generate_external_dataset(url):
    return extractor.generate_external_dataset(url)


@app.route('/api/crawl_url', methods=['POST'])
def crawl_url():
    try:
        data = request.json
        res = generate_external_dataset(data['url'])
        print (res);
        if res == 'Er':
            return jsonify({"error": "Something went wrong"}), 400
        return jsonify({"status": res})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/api/test', methods=['POST'])
def test_url():
    try:
        data = request.json
        res = generate_external_dataset("https://www.trovefinance.com/")
        return jsonify({"url_contents": data})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

# def main():
#     # Get user input
#
#     generate_external_dataset("https://www.trovefinance.com/")

if __name__ == '__main__':
    # main()
     app.run(debug=True)