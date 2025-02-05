#![cfg_attr(not(feature = "std"), no_std, no_main)]

#[ink::contract]
mod wallet {
    #[ink(storage)]
    pub struct Wallet {
        owner: AccountId,
        balance: Balance,
    }

    #[ink(event)]
    pub struct Deposit {
        #[ink(topic)]
        by: AccountId,
        amount: Balance,
    }

    #[ink(event)]
    pub struct Withdrawal {
        #[ink(topic)]
        by: AccountId,
        amount: Balance,
    }

    impl Wallet {
        #[ink(constructor)]
        pub fn new() -> Self {
            let caller = Self::env().caller();
            Self {
                owner: caller,
                balance: 0,
            }
        }

        #[ink(message, payable)]
        pub fn deposit(&mut self) {
            let amount = self.env().transferred_value();
            assert!(amount > 0, "Deposit amount must be greater than 0");
            self.balance = self.balance.checked_add(amount).expect("Balance overflow");
            self.env().emit_event(Deposit {
                by: self.env().caller(),
                amount,
            });
        }

        #[ink(message)]
        pub fn withdraw(&mut self, amount: Balance) {
            self.only_owner();
            self.balance = self.balance.checked_sub(amount)
                .expect("Insufficient funds");
            self.env().transfer(self.owner, amount).expect("Transfer failed");
            self.env().emit_event(Withdrawal {
                by: self.env().caller(),
                amount,
            });
        }

        #[ink(message)]
        pub fn get_balance(&self) -> Balance {
            self.balance
        }

        fn only_owner(&self) {
            assert_eq!(self.env().caller(), self.owner, "Only owner can withdraw funds");
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[ink::test]
        fn test_deposit_and_withdraw() {
            let mut contract = Wallet::new();

            // Simulate deposit transaction
            let deposit_amount = 100;
            ink::env::test::set_value_transferred::<ink::env::DefaultEnvironment>(deposit_amount);
            contract.deposit();

            assert_eq!(contract.get_balance(), deposit_amount);

            // Withdraw all funds
            let initial_balance = contract.get_balance();
            contract.withdraw(initial_balance);
            assert_eq!(contract.get_balance(), 0);
        }
    }


    // /// This is how you'd write end-to-end (E2E) or integration tests for ink! contracts.
    // ///
    // /// When running these you need to make sure that you:
    // /// - Compile the tests with the `e2e-tests` feature flag enabled (`--features e2e-tests`)
    // /// - Are running a Substrate node which contains `pallet-contracts` in the background
    // #[cfg(all(test, feature = "e2e-tests"))]
    // mod e2e_tests {
    //     /// Imports all the definitions from the outer scope so we can use them here.
    //     use super::*;

    //     /// A helper function used for calling contract messages.
    //     use ink_e2e::ContractsBackend;

    //     /// The End-to-End test `Result` type.
    //     type E2EResult<T> = std::result::Result<T, Box<dyn std::error::Error>>;

    //     /// We test that we can upload and instantiate the contract using its default constructor.
    //     #[ink_e2e::test]
    //     async fn default_works(mut client: ink_e2e::Client<C, E>) -> E2EResult<()> {
    //         // Given
    //         let mut constructor = WalletRef::default();

    //         // When
    //         let contract = client
    //             .instantiate("wallet", &ink_e2e::alice(), &mut constructor)
    //             .submit()
    //             .await
    //             .expect("instantiate failed");
    //         let call_builder = contract.call_builder::<Wallet>();

    //         // Then
    //         let get = call_builder.get();
    //         let get_result = client.call(&ink_e2e::alice(), &get).dry_run().await?;
    //         assert!(matches!(get_result.return_value(), false));

    //         Ok(())
    //     }

    //     /// We test that we can read and write a value from the on-chain contract.
    //     #[ink_e2e::test]
    //     async fn it_works(mut client: ink_e2e::Client<C, E>) -> E2EResult<()> {
    //         // Given
    //         let mut constructor = WalletRef::new(false);
    //         let contract = client
    //             .instantiate("wallet", &ink_e2e::bob(), &mut constructor)
    //             .submit()
    //             .await
    //             .expect("instantiate failed");
    //         let mut call_builder = contract.call_builder::<Wallet>();

    //         let get = call_builder.get();
    //         let get_result = client.call(&ink_e2e::bob(), &get).dry_run().await?;
    //         assert!(matches!(get_result.return_value(), false));

    //         // When
    //         let flip = call_builder.flip();
    //         let _flip_result = client
    //             .call(&ink_e2e::bob(), &flip)
    //             .submit()
    //             .await
    //             .expect("flip failed");

    //         // Then
    //         let get = call_builder.get();
    //         let get_result = client.call(&ink_e2e::bob(), &get).dry_run().await?;
    //         assert!(matches!(get_result.return_value(), true));

    //         Ok(())
    //     }
    // }
}
