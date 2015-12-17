import importlib
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
# from flask_swagger import swagger
from REST_UBER.uber_swagger import swagger
import pandas as pd
import REST_UBER.terrplant_rest


app = Flask(__name__)
api = Api(app)


# TODO: Generic API endpoint (TEMPORARY, remove once all endpoints are explicitly stated)
class ModelCaller(Resource):
    def get(self, model, jid):
        return {'result': 'model=%s, jid=%s' % (model, jid)}

    def post(self, model, jid):
        # TODO: Remove the YAML part of this docstring
        """
        Execute model
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
                address:
                  description: address for user
                  schema:
                    id: Address
                    properties:
                      street:
                        type: string
                      state:
                        type: string
                      country:
                        type: string
                      postalcode:
                        type: string
        responses:
          201:
            description: User created
        """
        try:
            # Dynamically import the model Python module
            model_module = importlib.import_module('.' + model + '_model_rest', model + '_rest')
            # Set the model Object to a local variable (class name = model)
            model_object = getattr(model_module, model)

            try:
                run_type = request.json["run_type"]
            except KeyError, e:
                return self.errorMessage(e, jid)

            if run_type == "qaqc":
                logging.info('============= QAQC Run =============')

                # pd_obj = pd.io.json.read_json(json.dumps(request.json["inputs"]))
                pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
                # pd_obj_exp = pd.io.json.read_json(json.dumps(request.json["out_exp"]))
                pd_obj_exp = pd.DataFrame.from_dict(request.json["out_exp"], dtype='float64')

                result_json_tuple = model_object(run_type, pd_obj, pd_obj_exp).json

            elif run_type == "batch":
                logging.info('============= Batch Run =============')
                # pd_obj = pd.io.json.read_json(json.dumps(request.json["inputs"]))
                pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')

                result_json_tuple = model_object(run_type, pd_obj, None).json

            else:
                logging.info('============= Single Run =============')
                pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')

                result_json_tuple = model_object(run_type, pd_obj, None).json

            # Values returned from model run: inputs, outputs, and expected outputs (if QAQC run)
            inputs_json = json.loads(result_json_tuple[0])
            outputs_json = json.loads(result_json_tuple[1])
            exp_out_json = json.loads(result_json_tuple[2])

            return {'user_id': 'admin',
                    'inputs': inputs_json,
                    'outputs': outputs_json,
                    'exp_out': exp_out_json,
                    '_id': jid,
                    'run_type': run_type}

        except Exception, e:
            return self.errorMessage(e, jid)

    def errorMessage(self, error, jid):
        """Returns exception error message as valid JSON string to caller"""
        logging.exception(error)
        e = str(error)
        return {'user_id': 'admin', 'result': {'error': e}, '_id': jid}


def errorMessage(error, jid):
    """Returns exception error message as valid JSON string to caller"""
    logging.exception(error)
    e = str(error)
    return {'user_id': 'admin', 'result': {'error': e}, '_id': jid}


# TODO: Used for THERPS, is this needed???
class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # or map(int, obj)
        return json.JSONEncoder.default(self, obj)


@app.route('/therps/<jid>', methods=['POST'])
def therps_rest(jid):
    all_result = {}
    try:
        for k, v in request.json.iteritems():
            exec '%s = v' % k
        all_result.setdefault(jid, {}).setdefault('status', 'none')
        from REST_UBER.therps_rest import therps_model_rest
        result = therps_model_rest.therps(chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, avian_ld50, avian_lc50,
                                          avian_NOAEC, avian_NOAEL,
                                          Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50,
                                          Species_of_the_tested_bird_avian_NOAEC,
                                          Species_of_the_tested_bird_avian_NOAEL,
                                          bw_avian_ld50, bw_avian_lc50, bw_avian_NOAEC, bw_avian_NOAEL,
                                          mineau_scaling_factor, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm,
                                          wp_herp_a_md,
                                          wp_herp_a_lg, c_mamm_a, c_herp_a)
        if (result):
            result_json = json.dumps(result.__dict__, cls=NumPyArangeEncoder)
            # all_result[jid]['status']='done'
            # all_result[jid]['input']=request.json
            # all_result[jid]['result']=result
        return json.dumps({'user_id': 'admin', 'result': result_json, '_id': jid})
    except Exception, e:
        return errorMessage(e, jid)


@app.route('/agdrift/<jid>', methods=['POST'])
def agdrift_rest(jid):
    all_result = {}
    try:
        for k, v in request.json.iteritems():
            exec '%s = v' % k
        all_result.setdefault(jid, {}).setdefault('status', 'none')
        from REST_UBER.agdrift_rest import agdrift_model_rest
        result = agdrift_model_rest.agdrift(drop_size, ecosystem_type, application_method, boom_height, orchard_type,
                                            application_rate, distance, aquatic_type, calculation_input,
                                            init_avg_dep_foa, avg_depo_gha, avg_depo_lbac, deposition_ngL,
                                            deposition_mgcm, nasae, y, x, express_y)
        if (result):
            # all_result[jid]['status']='done'
            # all_result[jid]['input']=request.json
            # all_result[jid]['result']=result
            return json.dumps({'user_id': 'admin', 'result': result.__dict__, '_id': jid})
    except Exception, e:
        return errorMessage(e, jid)


@app.route('/kabam/<jid>', methods=['POST'])
def kabam_rest(jid):
    all_result = {}
    try:
        for k, v in request.json.iteritems():
            exec '%s = v' % k
        all_result.setdefault(jid, {}).setdefault('status', 'none')
        from REST_UBER.kabam_rest import kabam_model_rest
        result = kabam_model_rest.kabam(chemical_name, l_kow, k_oc, c_wdp, water_column_EEC, c_wto,
                                        mineau_scaling_factor, x_poc, x_doc, c_ox, w_t, c_ss, oc, k_ow,
                                        Species_of_the_tested_bird, bw_quail, bw_duck, bwb_other, avian_ld50,
                                        avian_lc50, avian_noaec, m_species, bw_rat, bwm_other, mammalian_ld50,
                                        mammalian_lc50, mammalian_chronic_endpoint, lf_p_sediment, lf_p_phytoplankton,
                                        lf_p_zooplankton, lf_p_benthic_invertebrates, lf_p_filter_feeders,
                                        lf_p_small_fish, lf_p_medium_fish, mf_p_sediment, mf_p_phytoplankton,
                                        mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders,
                                        mf_p_small_fish, sf_p_sediment, sf_p_phytoplankton, sf_p_zooplankton,
                                        sf_p_benthic_invertebrates, sf_p_filter_feeders, ff_p_sediment,
                                        ff_p_phytoplankton, ff_p_zooplankton, ff_p_benthic_invertebrates,
                                        beninv_p_sediment, beninv_p_phytoplankton, beninv_p_zooplankton, zoo_p_sediment,
                                        zoo_p_phyto, s_lipid, s_NLOM, s_water, v_lb_phytoplankton, v_nb_phytoplankton,
                                        v_wb_phytoplankton, wb_zoo, v_lb_zoo, v_nb_zoo, v_wb_zoo, wb_beninv,
                                        v_lb_beninv, v_nb_beninv, v_wb_beninv, wb_ff, v_lb_ff, v_nb_ff, v_wb_ff, wb_sf,
                                        v_lb_sf, v_nb_sf, v_wb_sf, wb_mf, v_lb_mf, v_nb_mf, v_wb_mf, wb_lf, v_lb_lf,
                                        v_nb_lf, v_wb_lf, kg_phytoplankton, kd_phytoplankton, ke_phytoplankton,
                                        mo_phytoplankton, mp_phytoplankton, km_phytoplankton, km_zoo, k1_phytoplankton,
                                        k2_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k1_beninv, k2_beninv,
                                        kd_beninv, ke_beninv, km_beninv, k1_ff, k2_ff, kd_ff, ke_ff, km_ff, k1_sf,
                                        k2_sf, kd_sf, ke_sf, km_sf, k1_mf, k2_mf, kd_mf, ke_mf, km_mf, k1_lf, k2_lf,
                                        kd_lf, ke_lf, km_lf, rate_constants, s_respire, phyto_respire, zoo_respire,
                                        beninv_respire, ff_respire, sfish_respire, mfish_respire, lfish_respire)
        if (result):
            result_json = json.dumps(result.__dict__, cls=NumPyArangeEncoder)
            # all_result[jid]['status']='done'
            # all_result[jid]['input']=request.json
            # all_result[jid]['result']=result
            return json.dumps({'user_id': 'admin', 'result': result_json, '_id': jid})
    except Exception, e:
        return errorMessage(e, jid)


# TODO: Add model endpoints here once they are refactored
api.add_resource(REST_UBER.terrplant_rest.TerrplantHandler, '/terrplant/<string:jid>')
api.add_resource(ModelCaller, '/<string:model>/<string:jid>')  # Temporary generic route for API endpoints


@app.route("/api/spec")
def spec():
    """
    Route that returns the Swagger formatted JSON representing the Ubertool API.
    :return: Swagger formatted JSON string
    """
    swag = swagger(app)
    # Additional Swagger documentation key-values describing the ubertool API
    swag['info']['version'] = "0.1"
    swag['info']['title'] = u"\u00FCbertool API Documentation"
    swag['info']['description'] = "Welcome to the EPA's ubertool interactive RESTful API documentation."
    return jsonify(swag)


@app.route("/api")
def api_doc():
    """
    Route to serve the API documentation (Swagger UI) static page being served by the backend.
    :return:
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=7777, debug=True)