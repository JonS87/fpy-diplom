import { useState, useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { FaSort, FaPlus } from 'react-icons/fa';
import FileList from '../File/FileList/FileList';
import { logout, upload, loadFiles } from '../../redux/actions';
import logo from '../../assets/logo.jpg';
import userLogo from '../../assets/user.png';
import styles from './Dashboard.module.css';

export const Dashboard = () => {
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const [isDropdownVisible, setIsDropdownVisible] = useState(false);
    const [errorMessage, setErrorMessage] = useState(null);
    const [comment, setComment] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [isSortModalOpen, setIsSortModalOpen] = useState(false);
    const [sortField, setSortField] = useState('original_name');
    const [searchText, setSearchText] = useState('');
    const [sortOrder, setSortOrder] = useState('asc');
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user = useSelector((state) => state.user);
    const token = localStorage.getItem('token');
    const sortOptions = {
        user: 'Пользователь',
        original_name: 'Название',
        size: 'Размер',
        upload_date: 'Дата загрузки',
        last_download_date: 'Последняя дата скачивания',
        comment: 'Комментарий'
    };
    const sortModalRef = useRef();
    let searchTimeout;

    const handleLogout = () => {
        dispatch(logout());
        navigate('/');
    };

    const toggleProfileModal = () => {
        setIsProfileOpen(!isProfileOpen);
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
        }
    };

    const handleUpload = () => {
        if (selectedFile) {
            dispatch(upload(selectedFile, comment, token))
                .then(() => {
                    dispatch(loadFiles(token));
                    setIsModalOpen(false);
                    setComment('');
                    setSelectedFile(null);
                })
                .catch((error) => {
                    setErrorMessage("Ошибка загрузки файла: " + error.message);
                });
        }
    };

    const clearErrorMessage = () => {
        setErrorMessage(null);
    };

    const handleSortChange = (field) => {
        if (field === sortField) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortOrder('asc');
        }
        setIsSortModalOpen(false);
    };

    const handleSearchChange = (e) => {
        
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const value = e.target.value;
            setSearchText(value);
        }, 500);
    };

    const handleSortButtonClick = (event) => {
        const button = event.currentTarget;
        const { top, left, height } = button.getBoundingClientRect();
        
        setIsSortModalOpen(true);

        setTimeout(() => {
            if (sortModalRef.current) {
                sortModalRef.current.style.top = `${top + height}px`;
                sortModalRef.current.style.left = `${left}px`;
            }
        }, 0);
    };

    const handleClickOutside = (event) => {
        if (sortModalRef.current && !sortModalRef.current.contains(event.target)) {
            setIsSortModalOpen(false);
        }
    };

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    return (
        <div className={styles.dashboard}>
            {errorMessage && (
                <div className={styles.errorMessage} onClick={clearErrorMessage}>
                    {errorMessage}
                </div>
            )}
            <header className={styles.header}>
                <img src={logo} alt="MyCloud" className={styles.logo} />
                <div className={styles.actions}>
                    <input
                        type="text"
                        placeholder="Поиск файлов..."
                        className={styles.search}
                        onChange={handleSearchChange}
                    />
                {/* <div className={styles.actions}> */}
                    <button className={styles.sort} onClick={handleSortButtonClick}>
                        <FaSort />
                    </button>
                    <button
                        className={styles.add}
                        onClick={() => setIsModalOpen(true)}
                    >
                        <FaPlus />
                    </button>
                </div>
                    <div 
                        className={styles.userIcon}
                        onMouseEnter={() => setIsDropdownVisible(true)}
                        onMouseLeave={() => setIsDropdownVisible(false)}
                    >
                        <img
                            src={userLogo}
                            alt={user.username || 'Гость'}
                            className={styles.logo}
                        />
                        {isDropdownVisible && (
                            <div className={styles.dropdown}>
                                <button onClick={toggleProfileModal}>Профиль</button>
                                <button onClick={handleLogout}>Выйти</button>
                            </div>
                        )}
                    </div>
                {/* </div> */}
            </header>
            <main>
                <FileList searchText={searchText} sortField={sortField} sortOrder={sortOrder}/>
            </main>
            {isProfileOpen && (
                <div className={styles.profileModal}>
                    <h2>User Profile</h2>
                    <p>Username: {user.username}</p>
                    <button onClick={() => setIsProfileOpen(false)}>Закрыть</button>
                </div>
            )}
            {isModalOpen && (
                <div className={styles.modal}>
                    <h2>Добавить файл</h2>
                    <input type="file" onChange={handleFileChange} />
                    <input 
                        type="text" 
                        placeholder="Комментарий" 
                        value={comment} 
                        onChange={(e) => setComment(e.target.value)} 
                    />
                    <button onClick={handleUpload}>Отправить</button>
                    <button onClick={() => setIsModalOpen(false)}>Отмена</button>
                </div>
            )}
            {isSortModalOpen && (
                <div className={styles.sortModal} ref={sortModalRef}>
                    <h3>Выберите поле для сортировки</h3>
                    <ul>
                        {Object.keys(sortOptions).map(option => (
                            <li key={option} onClick={() => handleSortChange(option)}>
                                {sortOptions[option]}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};
