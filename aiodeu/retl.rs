use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyDict, PyList, PyFloat, PyInt, PyString, PyAny, PyLong};

use std::collections::HashMap;

// enum PyRecord {
//     // None,
//     String(PyString),
//     Integer(PyInt),
//     Float(PyFloat),
//     Long(PyLong),
//     // List(PyList),
//     // Dict(PyDict)
// }

// fn get_dict_value(py: Python, first_field: &str, dp: &str, dict: PyDict) -> PyRecord {
//     let val = dict.get_item(first_field);
//     return _get_field(dp, &val);
// }
//
// fn get_list_value(py: Python, dp: &str, list: PyList) -> PyRecord {
//     if !list.is_empty() {
//         let val = list.get_item(0);
//         return _get_field(dp, val);
//     }
//     PyString::new(py, "");
// }

fn _get_field(dot_path: &str, record: PyObject) -> PyObject {
    let field_parts: Vec<&str> = dot_path.split(".").collect();

    let first_field = field_parts[0];
    let remaining_fields = &field_parts[1..];
    let dp = remaining_fields.join(".");

    // match record {
    //     None => PyString::new(py, ""),
    //     Some(PyRecord::String(s)) => s,
    //     Some(PyRecord::Long(l)) => l,
    //     Some(PyRecord::Integer(i)) => i,
    //     Some(PyRecord::Float(f)) => f,
    //     // Some(PyRecord::Dict(d)) => get_dict_value(py, first_field, dp, d),
    //     // Some(PyRecord::List(l)) => get_list_value(py, dp, l),
    // }
    record
}

#[pyfunction(dot_path, record, name = "get_field")]
fn get_field(py: Python<'_>, dot_path: &str, record: &PyAny) -> PyResult<PyObject> {
    let field_parts: Vec<&str> = dot_path.split(".").collect();
    let field = field_parts[0];
    let remaining_fields = &field_parts[1..];
    let dp = remaining_fields.join(".");

    if field.is_empty() {
        if record.is_none() {
            Ok("".to_object(py))
        } else {
            Ok(record.to_object(py))
        }
    } else {
        let dict = record.extract::<HashMap<String, PyObject>>();
        match dict {
            Ok(d) => {
                let val = d.get(field);
                match val {
                    Some(v) => return get_field(py, dp.as_str(), v.as_ref(py)),
                    None => return Ok("".to_object(py)),
                }
            }
            Err(_) => (),
        }

        let list = record.extract::<Vec<PyObject>>();
        match list {
            Ok(l) => {
                if !l.is_empty() {
                    let d = l[0].extract::<HashMap<String, PyObject>>(py).unwrap();
                    let val = d.get(field);
                    match val {
                        Some(v) => return get_field(py, dp.as_str(), v.as_ref(py)),
                        None => return Ok("".to_object(py)),
                    }
                }
            }
            Err(_) => (),
        }

        if record.is_none() {
            return Ok("".to_object(py));
        }
        Ok(record.to_object(py))
    }
}


#[pymodule]
fn retl(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_field, m)?)?;
    Ok(())
}
