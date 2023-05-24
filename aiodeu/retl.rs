use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyDict, PyList, PyAny};
use std::collections::HashMap;

fn _get_hm_value(py: Python<'_>, hm: &HashMap<String, Py<PyAny>>, field: &str, dp: &String) -> PyObject {
    let val: Option<&Py<PyAny>> = hm.get(field);
    match val {
        Some(v) => {
            _get_field(py, dp.as_str(), v.as_ref(py))
        },
        None => "".to_object(py),
    }
}

fn _get_vec_value(py: Python<'_>, v: &Vec<Py<PyAny>>, field: &str, dp: &String) -> PyObject {
    if !v.is_empty() {
        let hm: Result<HashMap<String, Py<PyAny>>, PyErr> = v[0].extract::<HashMap<String, PyObject>>(py);
        match hm {
            Ok(d) => {
                _get_hm_value(py, &d, field, &dp)
            },
            Err(_) => "".to_object(py)
        }
    } else {
        "".to_object(py)
    }
}

fn _get_field(py: Python<'_>, dot_path: &str, any: &PyAny) -> PyObject {
    let field_parts: Vec<&str> = dot_path.split(".").collect();
    let field = field_parts[0];
    if any.is_none() {
        "".to_object(py)
    } else if field.is_empty() {
        any.to_object(py)
    } else {
        let remaining_fields = &field_parts[1..];
        let dp = remaining_fields.join(".");
        if let Ok(b) = py.is_instance::<PyDict, _>(any) {
            if b {
                let hm: HashMap<String, Py<PyAny>> = any.extract::<HashMap<String, PyObject>>().unwrap();
                return _get_hm_value(py, &hm, field, &dp);
            }
        }
        if let Ok(b) = py.is_instance::<PyList, _>(any) {
            if b {
                let v: Vec<Py<PyAny>> = any.extract::<Vec<PyObject>>().unwrap();
                return _get_vec_value(py, &v, field, &dp);
            }
        }
        any.to_object(py)
        // if let Ok(hm) = any.extract::<HashMap<String, PyObject>>() {
        //     _get_hm_value(py, &hm, field, &dp)
        // } else if let Ok(v) = any.extract::<Vec<PyObject>>() {
        //     _get_vec_value(py, &v, field, &dp)
        // } else {
        //     any.to_object(py)
        // }
    }
}

#[pyfunction(dot_path, record, name = "get_field")]
fn get_field(py: Python<'_>, dot_path: &str, record: &PyAny) -> PyResult<PyObject> {
    Ok(_get_field(py, dot_path, &record))
}

#[pymodule]
fn retl(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_field, m)?)?;
    Ok(())
}
