import {useState} from 'react';
import {useNavigate, Link} from 'react-router-dom';
import {login} from '../services/authService';

function Login(){
    const [email, setEmail]=useState('');
    const [password, setPassword]=useState('');
    const [error, setError]=useState('');
    const [loading, setLoading]=useState(false);
    const navigate=useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError('');
        setLoading(true);
        try {
            const data=await login(email, password);
            const role=data.role
            if (role==="customer"){
                navigate('/customerAccount');
            }
            // навигация по роли: добавить admin и manager
        } catch {
            setError('Неверный email или пароль');
        } finally {
            setLoading(false);
        }
    };

    return(
        <div style={{maxWidth:'400px', margin: '50px auto', padding: '20px' }}>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label>Адрес электронной почты:</label>
                    <input 
                        type="email"
                        value={email}
                        onChange={(event)=>setEmail(event.target.value)}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label>Пароль</label>
                    <input 
                        type="password"
                        value={password}
                        onChange={(event)=>setPassword(event.target.value)}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>
                {error && (
                    <div style={{ color: 'red', marginBottom: '10px', textAlign: 'center' }}>
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    style={{ 
                        width: '100%', 
                        padding: '10px',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        backgroundColor: loading ? '#ccc' : '#007bff', 
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px'
                    }}
                > {loading ? 'Вход...' : 'Войти'}
                </button>
            </form>

            <p style={{ marginTop: '15px', textAlign: 'center'  }}>
                Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
            </p>
        </div>
    );
}

export default Login;