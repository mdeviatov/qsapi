"""
This library consolidates Qlik Sense Engine API methods
"""

import json
import logging


async def create_app_objectlist(websocket, sid, handle):
    """
    Create a SessionList containing the App Object List.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Application
    :return: Handle for the session List
    """
    session_object = dict(
        jsonrpc='2.0',
        id=sid,
        handle=handle,
        method='CreateSessionObject',
        params=[
            dict(
                qInfo=dict(qType='AppLists'),
                qAppObjectListDef=dict(
                    qType='sheet',
                    qData=dict(id='/qInfo/qId')
                ),
                qDimensionListDef=dict(
                    qType='dimension',
                    qData={}
                ),
                qMeasureListDef=dict(
                    qType='measure'
                )
            )
        ]
    )
    await websocket.send(json.dumps(session_object))
    session_str = await websocket.recv()
    logging.info(f"< {session_str}")
    session_json = json.loads(session_str)
    return session_json['result']['qReturn']['qHandle']


async def get_all_infos(websocket, sid, handle):
    """
    This method returns the handle for a measure object.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Application
    :return:
    """
    all_infos_object = dict(
        jsonrpc='2.0',
        id=sid,
        handle=handle,
        method='GetAllInfos',
        params=dict()
    )
    await websocket.send(json.dumps(all_infos_object))
    all_infos_str = await websocket.recv()
    logging.info(f"< {all_infos_str}")
    return


async def get_app_layout(websocket, sid, handle):
    """
    This method returns the Application Layout information.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Application
    :return:
    """
    applayout_object = dict(
        jsonrpc='2.0',
        id=sid,
        handle=handle,
        method='GetAppLayout',
        params=dict()
    )
    await websocket.send(json.dumps(applayout_object))
    applayout_str = await websocket.recv()
    logging.info(f"< {applayout_str}")
    applayout_json = json.loads(applayout_str)
    return applayout_json['result']['qLayout']


async def get_child_infos(websocket, sid, handle):
    """
    This method returns the Child Info dictionary.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Parent
    :return:
    """
    all_infos_object = dict(
        jsonrpc='2.0',
        id=sid,
        handle=handle,
        method='GetChildInfos',
        params=dict()
    )
    await websocket.send(json.dumps(all_infos_object))
    all_infos_str = await websocket.recv()
    logging.info(f"< {all_infos_str}")
    all_infos_json = json.loads(all_infos_str)
    return all_infos_json['result']['qInfos']


async def get_dimension(websocket, sid, handle, qid):
    """
    This method returns the handle for a dimension object.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Application
    :param qid: Id for the dimension that need to be retrieved
    :return: Handle for the dimension
    """
    dimension_object = dict(
        jsonrpc='2.0',
        id=sid,
        handle=handle,
        method='GetDimension',
        params=dict(qId=qid)
    )
    await websocket.send(json.dumps(dimension_object))
    dimension_str = await websocket.recv()
    logging.info(f"< {dimension_str}")
    dimension_json = json.loads(dimension_str)
    return dimension_json['result']['qReturn']['qHandle']


async def get_doclist(websocket, sid):
    """
    Call GetDocList method from Global Class.

    :param websocket: Websocket connection handler.
    :param sid: Session ID
    :return: List of application dictionaries.
    """
    doclist = dict(
        jsonrpc='2.0',
        handle=-1,
        id=sid,
        method='GetDocList',
        params=[]
    )
    await websocket.send(json.dumps(doclist))
    docstr = await websocket.recv()
    logging.info(f"< {docstr}")
    docjson = json.loads(docstr)
    return docjson['result']['qDocList']


async def get_layout(websocket, sid, handle):
    """
    This method gets the Layout of the object with handle.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Application
    :return: Layout Dictionary
    """
    layout = dict(
        jsonrpc='2.0',
        handle=handle,
        id=sid,
        method='GetLayout',
        params=[]
    )
    await websocket.send(json.dumps(layout))
    layout_str = await websocket.recv()
    # pprint.pprint(layout_str, indent=4)
    logging.info(f"< {layout_str}")
    layout_json = json.loads(layout_str)
    return layout_json['result']['qLayout']


async def get_measure(websocket, sid, handle, qid):
    """
    This method returns the handle for a measure object.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Application
    :param qid: Id for the measure that need to be retrieved
    :return: Handle for the measure
    """
    measure_object = dict(
        jsonrpc='2.0',
        id=sid,
        handle=handle,
        method='GetMeasure',
        params=dict(qId=qid)
    )
    await websocket.send(json.dumps(measure_object))
    measure_str = await websocket.recv()
    logging.info(f"< {measure_str}")
    measure_json = json.loads(measure_str)
    return measure_json['result']['qReturn']['qHandle']


async def get_object(websocket, sid, handle, qid):
    """
    This method returns the handle for an object.

    :param websocket: Websocket connection for the handler
    :param sid: Session ID
    :param handle: Handle for the Parent
    :param qid: Id for the object that need to be retrieved
    :return: Handle for the object
    """
    obj = dict(
        jsonrpc='2.0',
        id=sid,
        handle=handle,
        method='GetObject',
        params=dict(qId=qid)
    )
    await websocket.send(json.dumps(obj))
    object_str = await websocket.recv()
    logging.info(f"< {object_str}")
    object_json = json.loads(object_str)
    return object_json['result']['qReturn']['qHandle']


async def get_script(websocket, sid, handle):
    """
    Calls the GetScript method from the Doc class.

    :param websocket: Websocket connection handler
    :param sid: Session ID
    :param handle: Handle ID for the method.
    :return: App script in bytestream format.
    """
    getscript = dict(
        jsonrpc='2.0',
        handle=handle,
        id=sid,
        method='GetScript',
        params={}
    )
    await websocket.send(json.dumps(getscript))
    script_str = await websocket.recv()
    logging.info(f"< {script_str}")
    script_json = json.loads(script_str)
    script = script_json['result']['qScript']
    return script


async def open_app(websocket, sid, app_id):
    """
    Calls the OpenDoc method from the Global class.

    :param websocket: Websocket connection handler
    :param sid: Session ID
    :param app_id: Application ID for application to open.
    :return: Application handle ID.
    """
    opendoc = dict(
        jsonrpc='2.0',
        handle=-1,
        id=sid,
        method='OpenDoc',
        # params=dict(
        #     qDocName=app_id,
        #     qNoData=True
        # )
        params=[app_id]
    )
    await websocket.send(json.dumps(opendoc))
    appstr = await websocket.recv()
    logging.info(f"< {appstr}")
    appjson = json.loads(appstr)
    handle = appjson['result']['qReturn']['qHandle']
    return handle
