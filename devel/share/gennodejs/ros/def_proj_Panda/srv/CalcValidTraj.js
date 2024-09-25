// Auto-generated. Do not edit!

// (in-package def_proj_Panda.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class CalcValidTrajRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.q_s = null;
      this.q_e = null;
      this.traj_duration = null;
      this.traj_step = null;
    }
    else {
      if (initObj.hasOwnProperty('q_s')) {
        this.q_s = initObj.q_s
      }
      else {
        this.q_s = [];
      }
      if (initObj.hasOwnProperty('q_e')) {
        this.q_e = initObj.q_e
      }
      else {
        this.q_e = [];
      }
      if (initObj.hasOwnProperty('traj_duration')) {
        this.traj_duration = initObj.traj_duration
      }
      else {
        this.traj_duration = 0.0;
      }
      if (initObj.hasOwnProperty('traj_step')) {
        this.traj_step = initObj.traj_step
      }
      else {
        this.traj_step = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type CalcValidTrajRequest
    // Serialize message field [q_s]
    bufferOffset = _arraySerializer.float64(obj.q_s, buffer, bufferOffset, null);
    // Serialize message field [q_e]
    bufferOffset = _arraySerializer.float64(obj.q_e, buffer, bufferOffset, null);
    // Serialize message field [traj_duration]
    bufferOffset = _serializer.float64(obj.traj_duration, buffer, bufferOffset);
    // Serialize message field [traj_step]
    bufferOffset = _serializer.float64(obj.traj_step, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type CalcValidTrajRequest
    let len;
    let data = new CalcValidTrajRequest(null);
    // Deserialize message field [q_s]
    data.q_s = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [q_e]
    data.q_e = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [traj_duration]
    data.traj_duration = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [traj_step]
    data.traj_step = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.q_s.length;
    length += 8 * object.q_e.length;
    return length + 24;
  }

  static datatype() {
    // Returns string type for a service object
    return 'def_proj_Panda/CalcValidTrajRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '847840f1b2b2579ff9a09bad22f082db';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] q_s
    float64[] q_e
    float64 traj_duration
    float64 traj_step
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new CalcValidTrajRequest(null);
    if (msg.q_s !== undefined) {
      resolved.q_s = msg.q_s;
    }
    else {
      resolved.q_s = []
    }

    if (msg.q_e !== undefined) {
      resolved.q_e = msg.q_e;
    }
    else {
      resolved.q_e = []
    }

    if (msg.traj_duration !== undefined) {
      resolved.traj_duration = msg.traj_duration;
    }
    else {
      resolved.traj_duration = 0.0
    }

    if (msg.traj_step !== undefined) {
      resolved.traj_step = msg.traj_step;
    }
    else {
      resolved.traj_step = 0.0
    }

    return resolved;
    }
};

class CalcValidTrajResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.flag_valid = null;
    }
    else {
      if (initObj.hasOwnProperty('flag_valid')) {
        this.flag_valid = initObj.flag_valid
      }
      else {
        this.flag_valid = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type CalcValidTrajResponse
    // Serialize message field [flag_valid]
    bufferOffset = _serializer.uint8(obj.flag_valid, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type CalcValidTrajResponse
    let len;
    let data = new CalcValidTrajResponse(null);
    // Deserialize message field [flag_valid]
    data.flag_valid = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'def_proj_Panda/CalcValidTrajResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9f8b8de568edd8c7dce07a786ddd4501';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 flag_valid
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new CalcValidTrajResponse(null);
    if (msg.flag_valid !== undefined) {
      resolved.flag_valid = msg.flag_valid;
    }
    else {
      resolved.flag_valid = 0
    }

    return resolved;
    }
};

module.exports = {
  Request: CalcValidTrajRequest,
  Response: CalcValidTrajResponse,
  md5sum() { return '70855c1f975352ceba80c99de40d0931'; },
  datatype() { return 'def_proj_Panda/CalcValidTraj'; }
};
