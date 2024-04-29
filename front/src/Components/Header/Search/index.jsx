import { useStates } from '../../../Hooks/useStates';
import { FilterList } from '../../Icons';

const Search = props => {
    const { s, f } = useStates();
    // s.show?.params
    const { styles } = props;

    const upgradeQ = e => {
        const value = e.target.value;
        f.u2('show', 'params', 'q', value);
    }

    const search = e => {
        e.preventDefault();
        f.u2('show', 'filtros', 'q', s.show?.params?.q);
    }

    return (
        <form 
            onSubmit={search}
            className={`${styles.search_container}`}>
            <input 
                type="text"
                className='rounded-xl py-1 px-3 text-black'
                placeholder='Search'
                value={s.show?.params?.q || ''}
                onChange={upgradeQ}
                />
            <span className={`${styles.filter_icon}`}>
                <FilterList
                     />
            </span>
        </form>
    )
}
export { Search }
