import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { register } from '../../../redux/actions';
import { useNavigate } from 'react-router-dom';
import styles from './Register.module.css';

export const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await dispatch(register({ username, email, password }));
            navigate('/files');
        } catch (err) {
            console.error(err);
            setError("Registration failed. Please try again.");
        }
    };

    return (
        <form className={styles["register-form"]} onSubmit={handleSubmit}>
            <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
            <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} autoComplete="email" />
            <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} autoComplete="new-password" />
            <button type="submit">Register</button>
            {error && <p className={styles.error}>{error}</p>}
        </form>
    );
};
