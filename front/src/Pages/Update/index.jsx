import { useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';
import styles from './styles/index.module.scss';

import { ColorsCubesUpdate } from '../../Components/Loaders/ColorsCubesUpdate';

const Update = props => {
    const { l, s, f  } = useStates();
    const userLogged = useMemo(() => s.login?.data?.user || {}, [s.login?.data?.user]);
    const updating = useMemo(() => !!s.loaders?.update?.updateNew, [s.loaders?.update?.updateNew]);

    const submit = e  => {
        if (!!e) e.preventDefault();
        const form = new FormData();
        form.append('file', document.getElementById('update_file').files[0]);
        form.append('base_name', s.update?.form?.base_name);
        form.append('cats', s.update?.form?.cats);
        f.update.updateNew(form);
    }

    if (!userLogged.token) {
        return (
            <div className='w-full flex justify-center'>
                <p className='text-3xl font-bold'>
                    Not logged
                </p>
            </div>
        );
    }

    if (updating) {
        return (
            <div className='w-full flex justify-center'>
                <ColorsCubesUpdate />
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <h1>Update</h1>
            <form className='flex flex-col' onSubmit={submit}>
                <div className='flex flex-col mt-3 p-5 w-10/12 md:w-1/3'>
                    <label htmlFor="">File</label>
                    <input type='file' id="update_file" name="file"/>
                </div>
                <div className='flex flex-col px-5 w-10/12 md:w-1/3'>
                    <label htmlFor="">Base name</label>
                    <input type='text' id="update_base_name" 
                        className='text-black py-1 px-3 rounded-lg mt-1'
                        value={s.update?.form?.base_name || ''}
                        onChange={e => f.u2('update', 'form', 'base_name', e.target.value)}
                        />
                </div>
                <div className='flex flex-col px-5 w-10/12 md:w-1/3'>
                    <label htmlFor="">Cats</label>
                    <input type='text' id="update_cats" 
                        className='text-black py-1 px-3 rounded-lg mt-1'
                        value={s.update?.form?.cats || ''}
                        onChange={e => f.u2('update', 'form', 'cats', e.target.value)}
                        />
                </div>
                <div className='flex flex-col px-5 w-10/12 md:w-1/3'>
                    <label htmlFor="">Scale</label>
                    <input type='text' id="update_scale" 
                        className='text-black py-1 px-3 rounded-lg mt-1'
                        value={s.update?.form?.scale || '2'}
                        onChange={e => f.u2('update', 'form', 'scale', e.target.value)}
                        />
                </div>

                <div className='flex flex-col px-5 w-10/12 md:w-1/3'>
                    <button type='submit' className='bg-blue-500 text-white rounded-lg mt-3 py-1'>
                        Update
                    </button>
                </div>
            </form>
            {/* input text */}
        </div>
    )
}

export { Update };