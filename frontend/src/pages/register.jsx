import {useState} from 'react'
import {useNavigate, Link} from 'react-router-dom' 
import {register} from '../services/authService'
import {useAuth} from '../services/AuthContext'

function Register(){
    const [name, setName]=useState('');
    const [email, setEmail]=useState('');
    const [password, setPassword]=useState('');
    const [error, setError]=useState('');
    const [loading, setLoading]=useState(false);
    const navigate=useNavigate();
    const { login } = useAuth();
    
    const handleSubmit = async (event) => {
            event.preventDefault();
            setError('');
            setLoading(true);
            try {
                await register({name, email, password});
                // После регистрации делаем логин через AuthContext
                await login(email, password);
                navigate('/account');
            } catch (err) {
                console.error('Registration error:', err);
                setError('Упс! Ошибка регистрации. Возможно, этот адрес электронной почты уже занят');
            } finally {
                setLoading(false);
            }
        };
        return(
        <div style={{maxWidth:'400px', margin: '50px auto', padding: '20px' }}>
            <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Регистрация</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label>Имя пользователя:</label>
                    <input 
                        type="text"
                        value={name}
                        onChange={(event)=>setName(event.target.value)}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>
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
                > {loading ? 'Регистрация...' : 'Зарегистрироваться'}
                </button>
            </form>
            <div style={{ textAlign: 'center', marginTop: '15px' }}>
                Уже есть аккаунт? <Link to="/login">Войти</Link>
            </div>
        </div>
    );
}

export default Register;

