from flask import Flask, render_template, request, jsonify
import time
import krpc

#KRPC Config

conn = krpc.connect(name='KRPC')
print('CONNECTED TO SPACE CENTER')

vessel = conn.space_center.active_vessel
ref_frame = vessel.orbit.body.reference_frame

met = conn.add_stream(getattr, vessel, 'met')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')

#Flask Config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/krpc/telem', methods=['GET'])
def krpc__telem():
    if request.method == 'GET':
        return jsonify(met=round(met()), altitude=round(altitude()), apoapsis=round(apoapsis()))

@app.route('/krpc/launch', methods=['GET'])
def krpc__launch():
    if request.method == 'GET':
        vessel.auto_pilot.target_pitch_and_heading(90, 90)
        vessel.auto_pilot.engage()
        vessel.control.throttle = 1
        vessel.control.activate_next_stage()

        return jsonify(status='go')
