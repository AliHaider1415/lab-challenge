import React, { useEffect, useState } from 'react'
import useAuth from '../hooks/useAuth'
import useUser from '../hooks/useUser'

export default function Home() {
    const { user, setUser } = useAuth()
    const getUser = useUser()
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchUser() {
            try {
                const fetchedUser = await getUser()
                setUser(fetchedUser)
            } catch (error) {
                console.error("Error fetching user data:", error)
            } finally {
                setLoading(false)
            }
        }

        fetchUser()
    }, [getUser, setUser])

    if (loading) {
        return <div className='container mt-3'>Loading...</div>
    }

    console.log(user)

    return (
        <div className='container mt-3'>
            <h2>
                <div className='row'>
                    <div className="mb-12">
                        {user?.email ? (
                            <>
                                <p>Email: {user.email}</p>
                                <p>Ethereum Balance: {user.ethereum_balance} ETH</p>
                            </>
                        ) : (
                            'Please login first'
                        )}
                    </div>
                </div>
            </h2>
        </div>
    )
}
