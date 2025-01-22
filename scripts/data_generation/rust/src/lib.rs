use pyo3::prelude::*;
use rand::prelude::*;
use rand::SeedableRng;
use rand_chacha::ChaCha8Rng;


fn mallows_insert_distributions(num_alternatives: usize, phi: f64) -> Vec<Vec<f64>> {
    let mut distributions = Vec::with_capacity(num_alternatives + 1);
    distributions.push(vec![]); 
    for i in 1..=num_alternatives {
        // Start with an empty distro of length i
        let mut distribution = vec![0.0; i];
        // compute the denom = phi^0 + phi^1 + ... phi^(i-1)
        let denominator: f64 = (0..i).map(|k| phi.powi(k as i32)).sum();
        // Fill each element of the distro with phi^(i-j) / denominator
        for j in 1..=i {
            distribution[j - 1] = phi.powi((i - j) as i32) / denominator;
        }
        distributions.push(distribution);
    }
    distributions
}

#[pyfunction]
#[pyo3(signature = (num_candidates, num_voters, phi, original_priority, seed=None))]
fn generate_mallows_votes(
    num_candidates: usize,
    num_voters: usize,
    phi: f64,
    original_priority: Vec<usize>,
    seed: Option<u64>,
) -> PyResult<Vec<Vec<usize>>> {
    if !(0.0..=1.0).contains(&phi) {
        return Err(pyo3::exceptions::PyValueError::new_err(
            format!("phi must be in [0, 1], got {}", phi)
        ));
    }

    // Precompute the distributions
    let insert_distributions = mallows_insert_distributions(num_candidates, phi);

    let mut rng = if let Some(s) = seed {
        ChaCha8Rng::seed_from_u64(s)
    } else {
        ChaCha8Rng::from_entropy()
    };

    let mut votes = Vec::with_capacity(num_voters);

    for _ in 0..num_voters {
        let mut insert_vector = vec![0; num_candidates];
        
        for i in 1..=num_candidates {
            let dist = &insert_distributions[i];
            let r: f64 = rng.gen();
            let mut cumsum = 0.0;
            let mut selected_pos = 1;
            
            for (j, &p) in dist.iter().enumerate() {
                cumsum += p;
                if r <= cumsum {
                    selected_pos = j + 1;
                    break;
                }
            }
            
            insert_vector[i-1] = selected_pos;
        }

        let mut vote = Vec::with_capacity(num_candidates);
        for i in 0..num_candidates {
            let pos = insert_vector[i] - 1;
            vote.insert(pos, original_priority[i]);
        }
        
        votes.push(vote);
    }

    Ok(votes)
}


#[pymodule]
fn mallows(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(generate_mallows_votes))?;
    Ok(())
}