import { useMemo } from 'react';
import { useStates } from '../../../Hooks/useStates';

import { HamburgerButton } from '../../Buttons';

import { GeneralModal } from '../../Modals/GeneralModal';
import { MenuModal } from './MenuModal';
import { Login } from './Login';

const Menu = props => {
    const { s, f } = useStates();
    const { styles } = props;
    const value = useMemo(() => !!s.modals?.header?.showMenu, [s.modals?.header?.showMenu]);
    const menuMode = useMemo(() => s.menu?.modal?.mode, [s.menu?.modal?.mode]);
    
    const update = value => {
        f.u2('modals', 'header', 'showMenu', value);
    }
    const onClick = e => {
        if (!!e) e.preventDefault();
        f.u2('modals', 'header', 'showMenu', !value);
    }
    return (
        <>
            <HamburgerButton
                value={value}
                update={update}
                onClick={onClick}
                />

            {s.modals?.header?.showMenu &&
            <GeneralModal
                Component={menuMode === 'login' ? Login : MenuModal}
                lvl1={'header'}
                lvl2={'showMenu'}
                modal_container_w="50"
                styles={styles}
                keyExec={menuMode === 'login' ? false : null}
                />}
        </>
    )
}

export { Menu }
